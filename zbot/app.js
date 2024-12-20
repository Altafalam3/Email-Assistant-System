import express from 'express';

const app = express();
const port = 8801;

import bodyParser from 'body-parser';
import qrcode from "qrcode-terminal";
import WhatsAppWeb from "whatsapp-web.js";
import axios from "axios";
import PDFDocument from "pdfkit";
import fs from "fs";
import { stringify } from 'csv-stringify';

const { Client, LocalAuth, MessageMedia } = WhatsAppWeb;

// bot -----------
const client = new Client({
   authStrategy: new LocalAuth(),
});

client.initialize();

client.on("qr", (qr) => {
   qrcode.generate(qr, { small: true });
   console.log("QR RECEIVED", qr);
});

client.on("authenticated", () => {
   console.log("AUTHENTICATED");
});

client.on("ready", () => {
   console.log("Client is ready!");
});

client.on("auth_failure", (msg) => {
   console.error("Authentication failed:", msg);
});

client.on("disconnected", (reason) => {
   console.error("Client was disconnected:", reason);
});

// middleware
app.use(bodyParser.json());

//  notification
app.post('/api/notification', async (req, res) => {
   const { number, message } = req.body;
   console.log(req.body);

   // if (!details || !companyName || !date) {
   //    return res.status(400).json({ error: 'Invalid request. Phone number and details are required.' });
   // }

   try {
      await emailNotification(number, message);

      res.status(200).json({ success: true, message: 'Booking notification sent successfully.' });
   } catch (error) {
      console.error('Error sending booking notification:', error);
      res.status(500).json({ error: 'Internal server error.' });
   }
});


async function emailNotification(number, message) {
   try {
      const chatNum = `91${number}@c.us`;
      await client.sendMessage(chatNum, message);
      console.log("done");
   } catch (error) {
      console.error('Error sending WhatsApp message:', error);
   }
}


//Replying Messages
client.on("message", async (message) => {
   const chatId = message.from;
   const text = message.body.toLowerCase();
   console.log(chatId, text);

   if (text === "hello") {
      client.sendMessage(chatId, "message is");
   }

   else if (text === "hi") {
      message.reply("Hiiiii");
   }
});


// connection
app.listen(port, () => {
   console.log(`Bot Server is running on port ${port}`);
});

require('dotenv').config(); // Load environment variables from .env file
const express = require('express');
const cors = require('cors');
const db = require('./db'); // We'll create this db connection module next
//for files
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5001; // Use a port like 5001 to avoid conflict with React's default 3000

// --- Middleware ---
// Enable CORS for all origins (adjust in production for security)
app.use(cors());
// Parse JSON request bodies
app.use(express.json());

// --- API Routes ---

// GET /api/apartments - post all apartments
// POST /api/apartments - Add a new apartment
app.post('/api/apartments', async (req, res) => {
    // Assuming 'db' is your configured database client (e.g., from 'pg' library)
    // Assuming this code is inside an async function (e.g., async (req, res) => { ... })

    const {
        apartment_name,
        apartment_address,
        apartment_description,
        apartment_rent_price,
        apartment_deposit_amount,
        apartment_availability_date,
        apartment_lease_length,
        apartment_images, // Assuming this is an array of strings (URLs)
        apartment_videos // Assuming this is an array of strings (URLs)
    } = req.body;

    // Basic Validation Example (add more robust validation as needed)
    if (!apartment_name || !apartment_address || !apartment_rent_price || !apartment_availability_date) {
        return res.status(400).json({ error: 'Missing required apartment fields.' });
    }

    try {
        // Use positional placeholders ($1, $2, ...)
        const queryText = `
      INSERT INTO apartments (
        ap_name,
        ap_address,
        ap_description,
        ap_rent_price,
        ap_deposit_amount,
        ap_availability_date,
        ap_lease_length,
        ap_image_urls,  -- Ensure this column type can handle arrays (e.g., TEXT[], VARCHAR[], JSONB)
        ap_video_url   -- Ensure this column type can handle arrays
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      RETURNING *`; // RETURNING * is good practice to get the inserted row

        // Create the values array with ALL the destructured variables
        // in the CORRECT order corresponding to the placeholders ($1, $2, ...)
        const values = [
            apartment_name,              // $1
            apartment_address,           // $2
            apartment_description,       // $3
            apartment_rent_price,        // $4 - Ensure this is a number if the DB column is numeric
            apartment_deposit_amount,    // $5 - Ensure this is a number or null
            apartment_availability_date, // $6 - Ensure this is a date/timestamp format DB accepts
            apartment_lease_length,      // $7 - Ensure this is suitable type (e.g., integer, text)
            apartment_images,            // $8 - Pass the array directly if DB column is array type (e.g., TEXT[])
            apartment_videos             // $9 - Pass the array directly if DB column is array type
        ];

        // Execute the query with the text and the ordered values
        const result = await db.query(queryText, values);

        // Corrected console log message
        console.log('Apartment added:', result.rows[0]);

        // Send back the newly created apartment data with 201 Created status
        res.status(201).json(result.rows[0]);

    } catch (error) {
        // Add error handling
        console.error('Error adding apartment:', error);
        res.status(500).json({ error: 'Internal server error while adding apartment.' });
    }
});

// ===== NEW GET Route to fetch all apartments =====
app.get('/api/apartments', async (req, res) => {
    try {
        // Query the database to get all apartments
        // Selecting specific columns is often better than SELECT *, but * is okay here
        const queryText = 'SELECT * FROM apartments ORDER BY ap_name DESC'; // Example: order by name
        const result = await db.query(queryText);

        console.log(`Retrieved ${result.rows.length} apartments.`);
        res.status(200).json(result.rows); // Send the array of apartments back as JSON

    } catch (error) {
        console.error('Error retrieving apartments:', error);
        // Send a generic server error response
        res.status(500).json({ error: 'Failed to retrieve apartments from the database.' });
    }
});

// --- Start Server ---
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// --- File Upload Route ---

// Configure multer for file storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadPath = path.join(__dirname, 'uploads'); // Ensure this folder exists
        cb(null, uploadPath);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, `${uniqueSuffix}-${file.originalname}`);
    }
});

const upload = multer({ storage });

// POST /api/upload - Handle file uploads and update the database
// POST /api/upload - Handle file uploads and update the database
app.post('/api/upload', upload.array('images', 10), async (req, res) => { // Added a limit, e.g., 10 images
    const { recordno } = req.body; // Only recordno from req.body

    // 1. Check if files were uploaded by Multer
    if (!req.files || req.files.length === 0) {
        return res.status(400).json({ error: 'No files uploaded.' });
    }

    // 2. Check if recordno is provided
    if (!recordno) {
        return res.status(400).json({ error: 'Missing required field: recordno.' });
    }

    try {
        // // 3. Construct file paths for ALL uploaded files
        // const newImagePaths = req.files.map(file => `/uploads/${file.filename}`);

        // // 4. Decide how to handle existing images.
        // //    Option A: REPLACE existing images with new ones (simplest based on current client)
        // const imagesToStoreInDB = newImagePaths;

        const newImagePaths = req.files.map(file => `/uploads/${file.filename}`);

        // OPTION A: REPLACE existing images (current logic)
        // Explicitly stringify the array for the JSONB column
        const imagesJsonString = JSON.stringify(newImagePaths);

        //    Option B: APPEND new images to existing ones (requires client to send existing ones)
        //    If you want to append, the client would need to send existing image URLs, e.g., in a field `existingImageUrls`
        //    And you'd do something like:
        //    const existingImages = req.body.existingImageUrls ? JSON.parse(req.body.existingImageUrls) : [];
        //    const imagesToStoreInDB = [...existingImages, ...newImagePaths];
        //    For now, let's stick to Option A (REPLACE) as the client doesn't send existing ones.

        // 5. Update the specific record in the apartments table
        //    IMPORTANT: Change this query to use recordno as a direct ID if possible.
        //    Assuming 'recordno' corresponds to a unique ID column like 'ap_id'.
        //    If 'recordno' is truly an offset, your previous query is syntactically okay, but risky.
        // const queryText = `
        //     UPDATE apartments
        //     SET ap_image_urls = $1
        //     WHERE ap_id = $2  -- SAFER: Use a direct ID. Replace 'ap_id' with your actual primary key column
        //     RETURNING *;
        // `;
        //If you MUST use OFFSET (less safe):
        const queryText = `
            UPDATE apartments
            SET ap_image_urls = $1
            WHERE ctid = (
                SELECT ctid
                FROM apartments
                ORDER BY ap_name -- Or whatever order makes recordno make sense
                OFFSET $2 LIMIT 1
            )
            RETURNING *;
        `;

         // Pass the JSON string as the value for $1
         const values = [imagesJsonString, recordno];

         const result = await db.query(queryText, values);

        if (result.rows.length === 0) {
            // This could mean the recordno (ap_id) didn't exist, or the OFFSET query found nothing
            return res.status(404).json({ error: 'No record found to update with that ID/recordno.' });
        }

        console.log('Record updated:', result.rows[0]);
        // Send a success: true property if client expects it, or client adjusts
        res.status(200).json({
            success: true, // Added for client compatibility
            message: 'Files uploaded and record updated successfully.',
            updatedRecord: result.rows[0]
        });

    } catch (error) {
        console.error('Error updating record with uploaded file:', error);
        if (error instanceof multer.MulterError) {
            return res.status(400).json({ error: `Multer error: ${error.message}` });
        }
        // Log the specific PostgreSQL error code if available
        if (error.code === '22P02') { // '22P02' is invalid_text_representation for JSON
             console.error("PostgreSQL JSON parsing error. Check the data being sent to the 'ap_image_urls' column.");
        }
        res.status(500).json({ error: 'Failed to update record with uploaded file.', details: error.message });
    }
});

// It's also good practice to have a Multer-specific error handler
// after your routes if you haven't already, or handle it in-route as above.
// Example (place after all routes that use Multer):
// app.use((err, req, res, next) => {
//   if (err instanceof multer.MulterError) {
//     return res.status(400).json({ error: `Upload Error: ${err.message}`, code: err.code });
//   } else if (err) {
//     console.error(err);
//     return res.status(500).json({ error: "An unexpected error occurred." });
//   }
//   next();
// });

// GET /api/apartments/fifth - Fetch the fifth record in the apartments table
app.get('/api/apartments/fifth', async (req, res) => {
    try {
        const queryText = `
            SELECT * 
            FROM apartments
            OFFSET 4 LIMIT 1
        `; // OFFSET 4 skips the first 4 records, LIMIT 1 fetches the fifth record
        const result = await db.query(queryText);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No fifth record found.' });
        }

        res.status(200).json(result.rows[0]);
    } catch (error) {
        console.error('Error retrieving the fifth apartment:', error);
        res.status(500).json({ error: 'Failed to retrieve the fifth apartment from the database.' });
    }
});
// GET /api/apartments/images/:recordno - Fetch all images of a single record based on offset
app.get('/api/apartments/images/:recordno', async (req, res) => {
    const { recordno } = req.params;

    try {
        const queryText = `
            SELECT ap_image_urls
            FROM apartments
            WHERE ctid = (
                SELECT ctid
                FROM apartments
                ORDER BY ap_name -- Adjust the order if needed
                OFFSET $1 LIMIT 1
            )
        `;
        const values = [recordno];
        const result = await db.query(queryText, values);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No record found for the given offset.' });
        }

        res.status(200).json({ images: result.rows[0].ap_image_urls });
    } catch (error) {
        console.error('Error fetching images:', error);
        res.status(500).json({ error: 'Failed to fetch images from the database.' });
    }
});


//Stop-Process -Name node -Force; node {server.js}
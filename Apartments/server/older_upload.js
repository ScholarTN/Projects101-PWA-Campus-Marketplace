app.post('/api/upload', upload.array('images'), async (req, res) => {
    const { recordno, images } = req.body;

    if (!req.images) {
        return res.status(400).json({ error: 'No file uploaded.' });
    }

    if (!recordno || !images) {
        return res.status(400).json({ error: 'Missing required fields: recordno or images.' });
    }

    try {
        // Construct the file path for the uploaded file
        const filePath = `/uploads/${req.images.filename}`;

        // Add the uploaded file path to the images array
        const updatedImages = [...images, filePath];

        // Update the specific record in the apartments table
        const queryText = `
            UPDATE apartments
            SET ap_image_urls = $1
            WHERE ctid = (
                SELECT ctid
                FROM apartments
                ORDER BY ap_name
                OFFSET $2 LIMIT 1
            )
            RETURNING *;
        `;

        const values = [updatedImages, recordno]; // Subtract 1 because OFFSET is zero-based

        const result = await db.query(queryText, values);

        if (result.rows.length === 0) {
            return res.status(404).json({ error: 'No record found to update.' });
        }

        console.log('Record updated:', result.rows[0]);
        res.status(200).json({ message: 'File uploaded and record updated successfully.', updatedRecord: result.rows[0] });
    } catch (error) {
        console.error('Error updating record with uploaded file:', error);
        res.status(500).json({ error: 'Failed to update record with uploaded file.' });
    }
});
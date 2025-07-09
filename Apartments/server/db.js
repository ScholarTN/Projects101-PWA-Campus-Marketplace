const { Pool } = require('pg');

// Create a new pool instance using environment variables
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_DATABASE,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

// Test the connection (optional but recommended)
pool.connect((err, client, release) => {
    if (err) {
        return console.error('Error acquiring client', err.stack);
    }
    client.query('SELECT NOW()', (err, result) => {
        release(); // Release the client back to the pool
        if (err) {
            return console.error('Error executing query', err.stack);
        }
        console.log('Successfully connected to PostgreSQL database!');
        // console.log('Current time from DB:', result.rows[0].now);
    });
});

// Export the query function so it can be used elsewhere
module.exports = {
    query: (text, params) => pool.query(text, params),
};

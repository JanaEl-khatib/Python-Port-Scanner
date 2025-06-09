-- This SQL query retrieves all appointments that are scheduled for today or later.
-- It also includes various operations such as counting appointments, updating statuses, and deleting duplicates.
-- It assumes a PostgreSQL database setup.
-- Create the appointments table if it does not exist

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100),
    doctor_name VARCHAR(100),
    appointment_date DATE,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into the appointments table
-- This data is for demonstration purposes and can be modified as needed.
INSERT INTO appointments (patient_name, doctor_name, appointment_date, status) VALUES
('John Smith', 'Dr. Allen', '2025-06-10', 'Scheduled'),
('Jane Doe', 'Dr. Carter', '2025-06-05', 'Completed'),
('Alice Johnson', 'Dr. Allen', '2025-06-12', 'Scheduled'),
('Mark Brown', 'Dr. Carter', '2025-06-08', 'Canceled'),
('Olivia Davis', 'Dr. Allen', '2025-06-15', 'Scheduled');

-- Query to retrieve all appointments scheduled for today or later
SELECT * FROM appointments WHERE appointment_date >= CURRENT_DATE;

-- Additional operations on the appointments table
-- Count total appointments, scheduled appointments, and group by status
SELECT COUNT(*) FROM appointments;
-- Count total appointments that are scheduled
SELECT COUNT(*) AS total_appoints FROM appointments WHERE status = 'Scheduled';
-- Count total appointments grouped by status
SELECT status, COUNT(*) AS total FROM appointments GROUP BY status;

-- Update the status of specific appointments
SELECT * FROM appointments WHERE doctor_name = 'Dr. Allen';
-- Update the status of an appointment
UPDATE appointments SET status = 'Completed' WHERE id = 3;
-- Update the status of all appointments for a specific patient
UPDATE appointments SET status = 'Completed' WHERE patient_name = 'Alice Johnson';

-- Delete duplicate appointments based on patient name, doctor name, appointment date, and status
DELETE FROM appointments WHERE id NOT IN (
    SELECT MIN(id)
    FROM appointments
    GROUP BY patient_name, doctor_name, appointment_date, status
);

-- Delete appointments that are canceled
DELETE FROM appointments WHERE status = 'Canceled';

-- Final query to retrieve all appointments ordered by id in ascending order
SELECT * FROM appointments ORDER BY id ASC;


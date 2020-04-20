--
-- Payload Table and Indexes.
--

-- Create the payload database
CREATE TABLE IF NOT EXISTS `payload` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `event` VARCHAR(535) COLLATE BINARY NOT NULL ,
    `payload_item_name` TEXT COLLATE BINARY ,
    `payload_item_url` TEXT COLLATE BINARY ,
    `payload_created_at` VARCHAR(535) COLLATE BINARY ,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL ,
    `downloaded` INTEGER NOT NULL DEFAULT 0 ,
    `downloaded_at` DATETIME
);

-- Create indexes for searching
CREATE INDEX `idx_event` ON payload (`event`);
CREATE INDEX `idx_downloaded` ON payload (`downloaded`);

--
-- Downloads Table, Index and Foreign Keys.
--

-- Enable foreign key support.
PRAGMA foreign_keys = ON;

-- Create downloads table with foreign key.
CREATE TABLE IF NOT EXISTS `downloads` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `payload_id` INTEGER NOT NULL,
    `file_size` VARCHAR DEFAULT NULL,
    `status_code` INTEGER DEFAULT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY(`payload_id`) REFERENCES payload(`id`)
);

-- Unique index of payload_id.
CREATE UNIQUE INDEX `idx_payload_id` ON downloads(`payload_id`);

--
-- Uploads Table, Index and Foreign Keys.
--

-- Enable foreign key support.
PRAGMA foreign_keys = ON;

-- Create uploads table with foreign key.
CREATE TABLE IF NOT EXISTS `uploads` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    `download_id` INTEGER NOT NULL,
    `drive_id` TEXT COLLATE BINARY NOT NULL,
    `drive_name` TEXT COLLATE BINARY NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
     FOREIGN KEY(`download_id`) REFERENCES downloads(`id`)
);

-- Unique index of download_id.
CREATE UNIQUE INDEX `idx_download_id` ON uploads(`download_id`);

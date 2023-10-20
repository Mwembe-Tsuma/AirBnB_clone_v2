ALTER DATABASE hbnb_dev_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE users CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE amenities CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

ALTER TABLE states CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE cities DROP FOREIGN KEY cities_ibfk_1;
-- modify was her
ALTER TABLE cities CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE cities ADD CONSTRAINT cities_ibfk_1 FOREIGN KEY (state_id) REFERENCES states(id) ON DELETE CASCADE;



ALTER TABLE places CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE place_amenity CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE review CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



ALTER TABLE cities MODIFY state_id INT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- users, amenities, states, cities(state), places(city, user), place_amenity(place, amenity), reviews(user, place), 

CREATE TABLE users (
        email VARCHAR(128) NOT NULL,
        password VARCHAR(128) NOT NULL,
        first_name VARCHAR(128),
        last_name VARCHAR(128),
        id VARCHAR(60) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (id)
);


CREATE TABLE places (
        city_id VARCHAR(60) NOT NULL,
        user_id VARCHAR(60) NOT NULL,
        name VARCHAR(128) NOT NULL,
        description VARCHAR(1024),
        number_rooms INTEGER NOT NULL,
        number_bathrooms INTEGER NOT NULL,
        max_guest INTEGER NOT NULL,
        price_by_night INTEGER NOT NULL,
        latitude FLOAT,
        longitude FLOAT,
        id VARCHAR(60) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(city_id) REFERENCES cities (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        UNIQUE (id)
);


CREATE TABLE place_amenity (
        place_id VARCHAR(60) NOT NULL,
        amenity_id VARCHAR(60) NOT NULL,
        PRIMARY KEY (place_id, amenity_id),
        FOREIGN KEY(place_id) REFERENCES places (id),
        FOREIGN KEY(amenity_id) REFERENCES amenities (id)
);


CREATE TABLE reviews (
        text VARCHAR(1024) NOT NULL,
        place_id VARCHAR(60) NOT NULL,
        user_id VARCHAR(60) NOT NULL,
        id VARCHAR(60) NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(place_id) REFERENCES places (id),
        FOREIGN KEY(user_id) REFERENCES users (id),
        UNIQUE (id)
);




--  ---------------------------------------
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost';
SET PASSWORD FOR 'hbnb_dev'@'localhost' = 'hbnb_dev_pwd';
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
--  ---------------------------------------

 CREATE TABLE `users` (
  `email` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `states` (
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `cities` (
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `state_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `state_id` (`state_id`),
  CONSTRAINT `cities_ibfk_1` FOREIGN KEY (`state_id`) REFERENCES `states` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `places` (
  `city_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(1024) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `number_rooms` int NOT NULL,
  `number_bathrooms` int NOT NULL,
  `max_guest` int NOT NULL,
  `price_by_night` int NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `city_id` (`city_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `places_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`id`),
  CONSTRAINT `places_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `amenities` (
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `name` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


 CREATE TABLE `reviews` (
  `text` varchar(1024) COLLATE utf8mb4_unicode_ci NOT NULL,
  `place_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `place_id` (`place_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



CREATE TABLE `place_amenity` (
  `place_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amenity_id` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`place_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `place_amenity_ibfk_1` FOREIGN KEY (`place_id`) REFERENCES `places` (`id`),
  CONSTRAINT `place_amenity_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
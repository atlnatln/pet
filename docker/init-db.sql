-- ==============================================================================
-- 🐾 Database Initialization - PostgreSQL setup
-- ==============================================================================

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set timezone
SET timezone = 'Europe/Istanbul';

-- Create database user permissions
GRANT ALL PRIVILEGES ON DATABASE pet_platform_db TO pet_user;

-- Performance tuning
ALTER DATABASE pet_platform_db SET default_text_search_config = 'turkish';

CREATE DATABASE meetups;

CREATE TABLE events (
  id VARCHAR(20), figure out how long it should be set it to be index
  created BIGINT,
  description TEXT,
  duration INT,
  event_hosts_id INT,
  featured BOOLEAN,
  featured_photo_id INT,
  group_id INT,
  how_to_find_us TEXT,
  link TEXT,
  local_date DATE,
  local_time TIME,
  manual_attendance_count INT,
  name TEXT,
  plain_text_no_images_description TEXT,
  pro_is_email_shared BOOLEAN,
  rsvp_close_offset TIME,
  rsvp_limit SMALLINT,
  rsvp_open_offset TIME,
  series_id INT,
  time_since_epoch BIGINT,
  updated BIGINT,
  utc_offset INT,
  venue_id INT,
  visibility VARCHAR(15)
  waitlist_count INT,
  why TEXT,
  yes_rsvp_count INT
);

CREATE TABLE venue 
CREATE TABLE rsvp_rules(link this with id)
CREATE TABLE event_hosts;
CREATE TABLE featured_photo;
CREATE TABLE fee(link this with id);

CREATE DATABASE meetups;

CREATE TABLE events (
  id VARCHAR(20),
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
  visibility VARCHAR(14),
  waitlist_count INT,
  why TEXT,
  yes_rsvp_count INT
);

CREATE TABLE venue (
  address_1 TEXT,
  address_2 TEXT,
  address_3 TEXT,
  city VARCHAR(32),
  country CHAR(2)
  id INT,
  Localized_country_name VARCHAR(32),
  --lat and lon precision and scale based off this:
  --https://en.wikipedia.org/wiki/Decimal_degrees#Precision
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  name TEXT,
  phone VARCHAR(32),
  repinned BOOLEAN,
  state VARCHAR(2)
  zip VARCHAR(16)
);

CREATE TABLE rsvp_rules (
  event_id VARCHAR(20)
  close_time BIGINT,
  closed BOOLEAN,
  guest_limit INT,
  open_time BIGINT,
  refund_days SMALLINT,
  notes TEXT,
  event_cancellation_refund BOOLEAN,
  no_refund BOOLEAN,
  member_cancellation_refund BOOLEAN,
  event_rescheduled_refund BOOLEAN,
  waitlisting VARCHAR(7)
);

CREATE TABLE event_hosts;
CREATE TABLE featured_photo;
CREATE TABLE fee(link this with id);

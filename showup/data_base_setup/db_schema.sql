CREATE TABLE event (
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
  visibility VARCHAR(13),
  waitlist_count INT,
  why TEXT,
  yes_rsvp_count INT
);

CREATE INDEX id ON event (id);

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
  lat DOUBLE PRECISION, --look into postGIS
  lon DOUBLE PRECISION,
  name TEXT,
  phone VARCHAR(32),
  repinned BOOLEAN,
  state CHAR(2)
  zip VARCHAR(16)
);

CREATE INDEX id ON venue (id);

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
  waitlisting VARCHAR(6)
);

CREATE INDEX event_id ON rsvp_rules (event_id);

CREATE TABLE host(
  id INT,
  name TEXT,
  intro TEXT,
  photo_id INT,
  host_count INT,
  join_date BIGINT,
  role VARCHAR(19)
);

CREATE INDEX id ON host (id);

CREATE TABLE hosted(
  event_id VARCHAR(20),
  host_id INT
);

CREATE INDEX event_hosted ON hosted (event_id, host_id);

CREATE TABLE photo(
  base_url TEXT,
  highres_link TEXT,
  id INT,
  photo_link TEXT,
  thumb_link TEXT,
  type VARCHAR(6)
);

CREATE INDEX id ON photo (id);

CREATE TABLE fee(
  event_id VARCHAR(20),
  accepts VARCHAR(6),
  amount INT,
  currency CHAR(3),
  description TEXT,
  label TEXT,
  required, BOOLEAN
);

CREATE INDEX event_id ON fee (event_id);

CREATE TABLE group (
  id INT,
  created BIGINT,
  name TEXT,
  join_mode  VARCHAR(8),
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  urlname TEXT,
  who TEXT,
  localized_location TEXT,
  region VARCHAR(8),
  timezone
  pro_network_id
  category_id
  visibility
  key_photo_id
  photo
  questions_req BOOLEAN,
  photo_req BOOLEAN,
  past_event_count INT
);

CREATE TABLE join_questions (
  group_id INT,
  question TEXT
);

CREATE TABLE topic (
  id INT,
  name TEXT,
  urlkey TEXT,
  lang VARCHAR(8),
);

CREATE TABLE group_topics (
  group_id INT,
  topic_id INT
);

CREATE TABLE pro_network (

);

CREATE TABLE category (

);


CREATE TABLE series (

);

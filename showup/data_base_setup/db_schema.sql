CREATE TABLE event (
  id VARCHAR(20),
  meta_data_url TEXT,
  created BIGINT,
  description TEXT,
  duration INT,
  event_hosts_id INT,
  featured BOOLEAN,
  featured_photo_id INT,
  meetup_group_id INT,
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
  country CHAR(2),
  id INT,
  Localized_country_name VARCHAR(32),
  --lat and lon precision and scale based off this:
  --https://en.wikipedia.org/wiki/Decimal_degrees#Precision
  lat DOUBLE PRECISION, --look into postGIS
  lon DOUBLE PRECISION,
  name TEXT,
  phone VARCHAR(32),
  repinned BOOLEAN,
  state CHAR(2),
  zip VARCHAR(16)
);

CREATE TABLE rsvp_rules (
  event_id VARCHAR(20),
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

CREATE TABLE host(
  id INT,
  name TEXT,
  intro TEXT,
  photo_id INT,
  host_count INT,
  join_date BIGINT,
  role VARCHAR(19)
);


CREATE TABLE hosted (
  event_id VARCHAR(20),
  host_id INT
);


CREATE TABLE photo (
  id INT,
  base_url TEXT,
  highres_link TEXT,
  photo_link TEXT,
  thumb_link TEXT,
  type VARCHAR(6)
);


CREATE TABLE fee (
  event_id VARCHAR(20),
  accepts VARCHAR(6),
  amount INT,
  currency CHAR(3),
  description TEXT,
  label TEXT,
  required BOOLEAN
);


CREATE TABLE meetup_group (
  id INT,
  meta_data_url TEXT,
  created BIGINT,
  name TEXT,
  join_mode  VARCHAR(8),
  lat DOUBLE PRECISION,
  lon DOUBLE PRECISION,
  urlname TEXT,
  who TEXT,
  localized_location TEXT,
  region VARCHAR(8),
  timezone VARCHAR(64),
  pro_network_urlname TEXT,
  category_id SMALLINT,
  visibility VARCHAR(14),
  key_photo_id INT,
  questions_req BOOLEAN,
  photo_req BOOLEAN,
  past_event_count INT,
  members INT,
  description TEXT
);

CREATE TABLE group_questions (
  meetup_group_id INT,
  questions_id INT
);

CREATE TABLE questions (
  id INT,
  question TEXT
);

CREATE TABLE topic (
  id INT,
  name TEXT,
  urlkey TEXT,
  lang VARCHAR(8)
);

CREATE TABLE group_topics (
  group_id INT,
  topic_id INT
);

CREATE TABLE pro_network (
  urlname VARCHAR(100),
  name TEXT,
  number_of_groups INT,
  network_url TEXT
);

CREATE TABLE category (
  id SMALLINT,
  name VARCHAR(64),
  shortname VARCHAR(64),
  sortname VARCHAR(64)
);

CREATE TABLE series (
  id INT,
  description TEXT,
  end_date BIGINT,
  start_date BIGINT,
  template_event_id INT
);

CREATE TABLE monthly_series (
  series_id INT,
  days_of_week SMALLINT,
  series_interval SMALLINT,
  week_of_month SMALLINT
);

CREATE TABLE weekly_series (
  series_id INT,
  series_interval SMALLINT,
  monday BOOLEAN,
  tuesday BOOLEAN,
  wednesday BOOLEAN,
  thursday BOOLEAN,
  friday BOOLEAN,
  saturday BOOLEAN,
  sunday BOOLEAN
);

CREATE TABLE meta_data (
  url TEXT,
  rel_links TEXT,
  url_code SMALLINT,
  req_date DATE
);

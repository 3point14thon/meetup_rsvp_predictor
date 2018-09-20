CREATE INDEX id ON event (id);

CREATE INDEX id ON venue (id);

CREATE INDEX id ON rsvp_rules (event_id);

CREATE INDEX id ON host (id);

CREATE INDEX event_hosted ON hosted (event_id, host_id);

CREATE INDEX id ON photo (id);

CREATE INDEX event_id ON fee (event_id);

CREATE INDEX id ON meetup_group (id);

CREATE INDEX group_questions ON groupquestions (event_id, host_id);

CREATE INDEX id ON questions (id);

CREATE INDEX id ON topic (id);

CREATE INDEX urlname ON pro_network (urlname);

CREATE INDEX id ON category (id);

CREATE INDEX id ON series (id);

CREATE INDEX series_id ON monthly_series (series_id);

CREATE INDEX series_id ON weekly_series (series_id);

CREATE INDEX id ON category (id);

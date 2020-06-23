CREATE TABLE notification_logs
(
    isbn            char(13) PRIMARY KEY,
    author          varchar(200)             NOT NULL,
    title           varchar(200)             NOT NULL,
    publishing_date date                     NOT NULL DEFAULT now(),
    notified_at     timestamp with time zone NOT NULL DEFAULT now()
);
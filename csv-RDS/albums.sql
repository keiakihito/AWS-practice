create table albums
(
    album_id           serial
        primary key,
    title              text,
    composer           text,
    artist             text,
    conductor          text,
    orchestra          text,
    label              text,
    release_date       date,
    genre              text[],
    period             text,
    cover_url          text,
    s3_prefix          text,
    original_format    text,
    digitized_format   text,
    licensing_status   text,
    third_party_link   text,
    notes              text,
    has_metadata_entry boolean   default true,
    total_duration     interval,
    created_at         timestamp default CURRENT_TIMESTAMP
);

alter table albums
    owner to postgres;



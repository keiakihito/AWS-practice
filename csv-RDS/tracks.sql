create table tracks
(
    id                 serial
        primary key,
    album_id           integer
        references albums
            on delete cascade,
    track_no           integer,
    title              text,
    duration           interval,
    tags               text[],
    soloists           text,
    s3_key             text
        unique,
    preview_url        text,
    original_format    text,
    digitized_format   text,
    licensing_status   text,
    third_party_link   text,
    notes              text,
    has_metadata_entry boolean   default true,
    created_at         timestamp default CURRENT_TIMESTAMP
);

alter table tracks
    owner to postgres;



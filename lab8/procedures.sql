CREATE OR REPLACE PROCEDURE upsert_contact(
    p_username VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook
        WHERE username = p_username
    ) THEN

        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;

    ELSE

        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);

    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    usernames TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(usernames, 1)
    LOOP

        IF phones[i] ~ '^[0-9]{11}$' THEN

            INSERT INTO phonebook(username, phone)
            VALUES (usernames[i], phones[i]);

        ELSE

            RAISE NOTICE 'Invalid phone: %', phones[i];

        END IF;

    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(val TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = val
       OR phone = val;
END;
$$;
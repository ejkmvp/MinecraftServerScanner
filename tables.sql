-- =========================
-- Table: Server_Information
-- =========================
CREATE TABLE Server_Information (
    Scan_Time          TIMESTAMP NOT NULL,
    Server_Name        VARCHAR NOT NULL,
    IP_Address         INET NOT NULL,
    Server_MOTD        VARCHAR NOT NULL,
    Server_Favicon     VARCHAR NOT NULL,
    Max_Player_Count   INTEGER NOT NULL,

    PRIMARY KEY (
        Server_Name,
        IP_Address,
        Server_MOTD,
        Server_Favicon,
        Max_Player_Count
    )
);

-- =========================
-- Table: Player_Information
-- =========================
CREATE TABLE Player_Information (
    UUID      UUID NOT NULL,
    Username  VARCHAR NOT NULL,

    PRIMARY KEY (UUID)
);

-- =========================
-- Table: Connections
-- =========================
CREATE TABLE Connections (
    Scan_Time   TIMESTAMP NOT NULL,
    UUID        UUID NOT NULL,
    IP_Address  INET NOT NULL,

    PRIMARY KEY (Scan_Time, UUID, IP_Address)
);
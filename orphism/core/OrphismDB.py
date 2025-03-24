import sqlite3
import os
from datetime import datetime
import logging

class AudioDBSqlite:
    """
    Class for basic SQLite operations in AudioDB application.
    Handles database connection, table creation, and CRUD operations.
    """
    
    def __init__(self, db_path="audiodb.sqlite"):
        """
        Initialize the database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Set up logging for database operations"""
        logger = logging.getLogger('AudioDBSqlite')
        logger.setLevel(logging.DEBUG)
        
        # Create handler if it doesn't exist
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            # Add file handler
            if not os.path.exists('logs'):
                os.makedirs('logs')
            file_handler = logging.FileHandler('logs/database.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        return logger
    
    def connect(self):
        """Establish connection to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            self.cursor = self.connection.cursor()
            self.logger.info(f"Connected to database: {self.db_path}")
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            self.logger.info("Database connection closed")
    
    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            # Create audio files table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                duration REAL,
                size INTEGER,
                format TEXT,
                bitrate INTEGER,
                sample_rate INTEGER,
                channels INTEGER,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_played TIMESTAMP,
                play_count INTEGER DEFAULT 0,
                favorite BOOLEAN DEFAULT 0
            )
            ''')
            
            # Create playlists table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_modified TIMESTAMP
            )
            ''')
            
            # Create playlist_items table (for many-to-many relationship)
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist_items (
                playlist_id INTEGER,
                audio_id INTEGER,
                position INTEGER,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (playlist_id, audio_id),
                FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE,
                FOREIGN KEY (audio_id) REFERENCES audio_files (id) ON DELETE CASCADE
            )
            ''')
            
            # Create tags table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            ''')
            
            # Create audio_tags table (for many-to-many relationship)
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audio_tags (
                audio_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (audio_id, tag_id),
                FOREIGN KEY (audio_id) REFERENCES audio_files (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
            )
            ''')
            
            self.connection.commit()
            self.logger.info("Database tables initialized successfully")
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error initializing database: {e}")
            return False
    
    # CRUD operations for audio files
    
    def add_audio_file(self, filename, filepath, duration=None, size=None, 
                       format=None, bitrate=None, sample_rate=None, channels=None):
        """
        Add a new audio file to the database
        
        Args:
            filename (str): Name of the audio file
            filepath (str): Full path to the audio file
            duration (float): Duration in seconds
            size (int): File size in bytes
            format (str): Audio format (MP3, WAV, etc.)
            bitrate (int): Audio bitrate
            sample_rate (int): Sample rate in Hz
            channels (int): Number of audio channels
            
        Returns:
            int: ID of the newly added file, or None if failed
        """
        if not self.connection and not self.connect():
            return None
            
        try:
            self.cursor.execute('''
            INSERT INTO audio_files (filename, filepath, duration, size, format, 
                                    bitrate, sample_rate, channels, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (filename, filepath, duration, size, format, bitrate, 
                 sample_rate, channels, datetime.now()))
            
            self.connection.commit()
            last_id = self.cursor.lastrowid
            self.logger.info(f"Added audio file: {filename} (ID: {last_id})")
            return last_id
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error adding audio file {filename}: {e}")
            return None
    
    def get_audio_file(self, file_id):
        """
        Get audio file by ID
        
        Args:
            file_id (int): ID of the audio file
            
        Returns:
            dict: Audio file data or None if not found
        """
        if not self.connection and not self.connect():
            return None
            
        try:
            self.cursor.execute("SELECT * FROM audio_files WHERE id = ?", (file_id,))
            result = self.cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving audio file ID {file_id}: {e}")
            return None
    
    def get_all_audio_files(self, limit=None, offset=0, order_by="date_added", order="DESC"):
        """
        Get all audio files with optional pagination
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            order_by (str): Column to order by
            order (str): Order direction (ASC or DESC)
            
        Returns:
            list: List of audio files as dictionaries
        """
        if not self.connection and not self.connect():
            return []
            
        try:
            query = f"SELECT * FROM audio_files ORDER BY {order_by} {order}"
            
            if limit is not None:
                query += f" LIMIT {limit} OFFSET {offset}"
                
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving audio files: {e}")
            return []
    
    def update_audio_file(self, file_id, **kwargs):
        """
        Update audio file properties
        
        Args:
            file_id (int): ID of the audio file to update
            **kwargs: Fields to update (key=value pairs)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection and not self.connect():
            return False
            
        if not kwargs:
            return False
            
        try:
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(file_id)
            
            self.cursor.execute(
                f"UPDATE audio_files SET {set_clause} WHERE id = ?", 
                values
            )
            
            self.connection.commit()
            self.logger.info(f"Updated audio file ID {file_id}")
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error updating audio file ID {file_id}: {e}")
            return False
    
    def delete_audio_file(self, file_id):
        """
        Delete audio file from database
        
        Args:
            file_id (int): ID of the audio file to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection and not self.connect():
            return False
            
        try:
            self.cursor.execute("DELETE FROM audio_files WHERE id = ?", (file_id,))
            self.connection.commit()
            self.logger.info(f"Deleted audio file ID {file_id}")
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error deleting audio file ID {file_id}: {e}")
            return False
    
    # Playlist operations
    
    def create_playlist(self, name, description=None):
        """
        Create a new playlist
        
        Args:
            name (str): Name of the playlist
            description (str): Description of the playlist
            
        Returns:
            int: ID of the newly created playlist, or None if failed
        """
        if not self.connection and not self.connect():
            return None
            
        try:
            now = datetime.now()
            self.cursor.execute(
                "INSERT INTO playlists (name, description, date_created, last_modified) VALUES (?, ?, ?, ?)",
                (name, description, now, now)
            )
            
            self.connection.commit()
            last_id = self.cursor.lastrowid
            self.logger.info(f"Created playlist: {name} (ID: {last_id})")
            return last_id
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error creating playlist {name}: {e}")
            return None
    
    def add_to_playlist(self, playlist_id, audio_id, position=None):
        """
        Add an audio file to a playlist
        
        Args:
            playlist_id (int): ID of the playlist
            audio_id (int): ID of the audio file
            position (int): Position in the playlist (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection and not self.connect():
            return False
            
        try:
            # If position is not specified, add to the end
            if position is None:
                self.cursor.execute(
                    "SELECT COALESCE(MAX(position), 0) + 1 FROM playlist_items WHERE playlist_id = ?",
                    (playlist_id,)
                )
                position = self.cursor.fetchone()[0]
            
            self.cursor.execute(
                "INSERT INTO playlist_items (playlist_id, audio_id, position, date_added) VALUES (?, ?, ?, ?)",
                (playlist_id, audio_id, position, datetime.now())
            )
            
            # Update the last_modified timestamp of the playlist
            self.cursor.execute(
                "UPDATE playlists SET last_modified = ? WHERE id = ?",
                (datetime.now(), playlist_id)
            )
            
            self.connection.commit()
            self.logger.info(f"Added audio ID {audio_id} to playlist ID {playlist_id} at position {position}")
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Error adding audio to playlist: {e}")
            return False
    
    def execute_query(self, query, parameters=None):
        """
        Execute a custom SQL query
        
        Args:
            query (str): SQL query to execute
            parameters (tuple): Query parameters
            
        Returns:
            list: Query results as dictionaries
        """
        if not self.connection and not self.connect():
            return []
            
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
                
            if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                results = self.cursor.fetchall()
                return [dict(row) for row in results]
            else:
                self.connection.commit()
                return []
        except sqlite3.Error as e:
            if not query.strip().upper().startswith(("SELECT", "PRAGMA")):
                self.connection.rollback()
            self.logger.error(f"Error executing query: {e}")
            return []
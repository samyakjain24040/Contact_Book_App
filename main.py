"""
This module defines a ContactBookApp class, which is a Kivy app that
allows users to store and search for contact information in a MySQL
database.

The `ContactBookApp` class inherits from `App` and overrides the `build`
method to create a `BoxLayout` containing `TextInput` widgets for
entering contact information and a `RecycleView` to display the
contacts.

The `ContactBookApp` class has methods for connecting to the MySQL
database, loading data from the database into the `RecycleView`,
adding a new contact to the database, deleting a contact from the
database, and editing a contact in the database.

Attributes:
    conn (MySQLdb.connection): A connection to the MySQL database.
    name_text (TextInput): A `TextInput` widget for entering the name.
    number_text (TextInput): A `TextInput` widget for entering the
        contact number.
    email_text (TextInput): A `TextInput` widget for entering the email.
    address_text (TextInput): A `TextInput` widget for entering the
        address.
    recycleview (RecycleView): A `RecycleView` widget to display the
        contacts.

"""

import kivy
kivy.require('1.10.0')

import mysql.connector as MySQLdb

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView


class ContactBookApp(App):
    """
    The ContactBookApp is a Kivy application that allows users to interact
    with a MySQL database to manage contact information. The application
    provides functions to add, delete, search, and edit contact
    information.
    """

    def build(self) -> BoxLayout:
        """
        Builds the BoxLayout for the app.

        The layout contains text inputs for name, contact number, email,
        and address. Also includes a recycle view for displaying contact
        information and buttons for adding, deleting, searching, editing,
        and exiting the app.

        Returns
        -------
        BoxLayout
            The BoxLayout object containing the app's UI.
        """
        # Create the layout
        layout = BoxLayout(orientation='vertical')

        # Create the name text input
        self.name_text = self._create_text_input(layout, 'Name')

        # Create the contact number text input
        self.number_text = self._create_text_input(layout, 'Contact No.')

        # Create the email text input
        self.email_text = self._create_text_input(layout, 'Email')

        # Create the address text input
        self.address_text = self._create_text_input(layout, 'Address')

        # Create the recycle view
        self.recycleview = self._create_recycleview(layout)

        # Create the 'Add' button
        self._create_button(layout, 'Add', self.add_contact)

        # Create the 'Delete' button
        self._create_button(layout, 'Delete', self.delete_contact)

        # Create the 'Search' button
        self._create_button(layout, 'Search', self.search_contact)

        # Create the 'Edit' button
        self._create_button(layout, 'Edit', self.edit_contact)

        # Create the 'Exit' button
        self._create_button(layout, 'Exit', self.stop)

        # Connect to the database
        self.conn = self._connect_to_db()

        # Load the data from the database
        self.load_data()

        # Return the layout
        return layout

    def stop(self, _):
        """
        Closes the MySQL connection and stops the app.

        Parameters
        ----------
        _ : any
            Ignored parameter.

        This function stops the app by closing the MySQL connection and
        calling the base class's stop method.
        """
        # Close the MySQL connection
        self.conn.close()

        # Call the base class's stop method to stop the app
        # The base class is the app itself, so this will stop the app
        self.stop()

    def _connect_to_db(self) -> MySQLdb:
        """
        Connects to the MySQL database.

        This function attempts to establish a connection to the MySQL database
        using the provided credentials. If the connection is successful, it is
        returned. Otherwise, an error message is printed and the function raises
        the exception.

        Returns
        -------
        MySQLdb.Connection
            The connection to the MySQL database.
        """

        # Establish a connection to the MySQL database
        try:
            conn = MySQLdb.connect(
                host='localhost',  # The host name or IP address of the database server
                user='root',       # The username for the database connection
                password='(enter password)',    # The password for the database connection
                database='contact_book'  # The name of the database to connect to
            )
        except MySQLdb.Error as e:
            # Print an error message if the connection fails
            print(f"Error connecting to MySQL database: {e}")
            # Re-raise the exception to handle it in a higher level
            raise
        else:
            # Return the connection if the connection is successful
            return conn

    def _create_recycleview(self, layout: BoxLayout) -> RecycleView:
        """
        Creates a RecycleView and adds it to the layout.

        Parameters:
            layout (BoxLayout): The layout to add the RecycleView to.

        Returns:
            RecycleView: The created RecycleView.
        """
        # Create a RecycleView
        recycleview = RecycleView()

        # Add the RecycleView to the layout
        layout.add_widget(recycleview)

        # Return the created RecycleView
        return recycleview

    def _create_text_input(self, layout: BoxLayout, text: str) -> TextInput:
        """
        Creates a label and input pair in the layout.

        Parameters:
            layout (BoxLayout): The layout to add the label and input to.
            text (str): The text for the label.

        Returns:
            TextInput: The created text input.
        """
        # Create a label
        label = Label(text=text)

        # Add the label to the layout
        layout.add_widget(label)

        # Create a text input
        text_input = TextInput(text='', multiline=False)

        # Add the text input to the layout
        layout.add_widget(text_input)

        # Return the created text input
        return text_input

    def _create_button(self, layout: BoxLayout, text: str, on_press):
        """
        Create a button in the layout and return it.

        Parameters:
            layout (BoxLayout): The layout to add the button to.
            text (str): The text for the button.
            on_press (Callable): The function to call when the button is pressed.

        Returns:
            Button: The created button.
        """
        # Create a button
        # The button will display the provided text and call the provided function when pressed.
        button = Button(text=text, on_press=on_press)

        # Add the button to the layout
        # The button will be displayed in the layout.
        layout.add_widget(button)

        # Return the created button
        return button

    def _create_label(self, layout: BoxLayout, text: str):
        """
        Creates a label in the layout.

        Parameters:
            layout (BoxLayout): The layout to add the label to.
            text (str): The text for the label.
        Returns:
            Label: The created label.
        """
        # Create a label with the given text
        label = Label(text=text)

        # Add the label to the layout
        layout.add_widget(label)

        # Return the created label
        return label

    def load_data(self):
        """
        Load data from the database into the RecycleView.

        This function executes a SELECT query on the 'contacts' table in the database
        and populates the RecycleView with the fetched data.

        Parameters:
            None

        Returns:
            None
        """
        try:
            # Create a database cursor
            cursor = self.conn.cursor()

            # Execute a SELECT query to fetch all the rows from the 'contacts' table
            cursor.execute("SELECT * FROM contacts")

            # Fetch all the rows as a list of tuples
            rows = cursor.fetchall()

            # Create a list of dictionaries with the fetched data
            data = [{'Name': row[0], 'Number': row[1],
                    'Email': row[2], 'Address': row[3]}
                    for row in rows]

            # Update the RecycleView with the fetched data
            self.recycleview.data = data

        except MySQLdb.Error as e:
            # Print an error message if there is an error loading data from the database
            print(f"Error loading data from MySQL database: {e}")

        finally:
            # Close the database cursor
            cursor.close()

    def add_contact(self, _):
        """
        Adds a new contact to the database.

        This function executes an INSERT query to add a new contact to the
        'contacts' table in the MySQL database. The contact's information is
        extracted from the text inputs of the app.

        Args:
            _: Ignored parameter.

        Returns:
            None
        """
        try:
            # Create a database cursor
            cursor = self.conn.cursor()

            # Prepare the SQL query to insert a new contact
            query = "INSERT INTO contacts (name, number, email, address) VALUES (%s, %s, %s, %s)"

            # Extract the contact information from the text inputs
            contact_info = (self.name_text.text, self.number_text.text,
                            self.email_text.text, self.address_text.text)

            # Execute the query with the contact information
            cursor.execute(query, contact_info)

            # Commit the changes to the database
            self.conn.commit()

            # Load the updated data into the RecycleView
            self.load_data()

        except MySQLdb.Error as e:
            # Print an error message if there is an error adding a contact to the database
            print(f"Error adding contact to MySQL database: {e}")

        finally:
            # Close the database cursor
            cursor.close()

    def delete_contact(self, _):
        """
        Deletes a contact from the database.

        Args:
            _: A dummy argument, unused in this function.

        This function deletes a contact from the MySQL database based on the contact's number.
        It executes a SQL query to delete the contact, commits the changes to the database,
        and reloads the data into the RecycleView. If there is an error, it prints the error message.
        Regardless of the outcome, it closes the database cursor.
        """
        try:
            # Create a database cursor
            cursor = self.conn.cursor()

            # Prepare the SQL query to delete the contact
            query = "DELETE FROM contacts WHERE number = %s"

            # Execute the query with the contact's number
            cursor.execute(query, (self.number_text.text,))

            # Commit the changes to the database
            self.conn.commit()

            # Load the updated data into the RecycleView
            self.load_data()

        except MySQLdb.Error as e:
            # Print an error message if there is an error deleting the contact from the database
            print(f"Error deleting contact from MySQL database: {e}")

        finally:
            # Close the database cursor
            cursor.close()
            
    def search_contact(self, _):
        """
        Searches for a contact in the database and displays the result.

        Args:
            _: A dummy argument, unused in this function.

        This function executes a SQL query to search for a contact in the MySQL database
        based on the contact's number. It retrieves the contact's information and
        displays it in a label. If the contact is not found, it displays a message
        indicating that the contact was not found. Regardless of the outcome, it closes
        the database cursor and returns True.
        """
        try:
            # Create a database cursor
            cursor = self.conn.cursor()

            # Prepare the SQL query to search for the contact
            query = "SELECT * FROM contacts WHERE number = %s"

            # Execute the query with the contact's number
            cursor.execute(query, (self.number_text.text,))

            # Retrieve the contact's information
            row = cursor.fetchone()

            if row:
                # Contact found, format the output
                output = f"Contact found:\nName: {row[0]}\nNumber: {row[1]}\nEmail: {row[2]}\nAddress: {row[3]}"
            else:
                # Contact not found, display a message
                output = "Contact not found."

            # Clear the text fields
            self.name_text.text = ''
            self.number_text.text = ''
            self.email_text.text = ''
            self.address_text.text = ''

            # Display the output in a label
            self.output_label.text = output

        except MySQLdb.Error as e:
            # Print an error message if there is an error searching for the contact in the database
            print(f"Error searching contact in MySQL database: {e}")

        finally:
            # Close the database cursor and return True
            cursor.close()
            return True
    def edit_contact(self, _):
        """
        Edits a contact in the database.

        This function executes an UPDATE query to edit a contact in the
        'contacts' table in the MySQL database. The contact's information is
        extracted from the text inputs of the app and the contact is identified
        by its number.

        Args:
            _: Ignored parameter.

        Returns:
            None
        """
        try:
            # Create a database cursor
            cursor = self.conn.cursor()

            # Prepare the SQL query to edit a contact
            query = """
                UPDATE contacts
                SET name = %s, number = %s, email = %s, address = %s
                WHERE number = %s
            """

            # Extract the contact information from the text inputs
            contact_info = (self.name_text.text, self.number_text.text,
                            self.email_text.text, self.address_text.text,
                            self.number_text.text)

            # Execute the query with the contact information
            cursor.execute(query, contact_info)

            # Commit the changes to the database
            self.conn.commit()

            # Load the updated data into the RecycleView
            self.load_data()

        except MySQLdb.Error as e:
            # Print an error message if there is an error editing the contact in the database
            print(f"Error editing contact in MySQL database: {e}")
        finally:
            # Close the database cursor
            cursor.close()

# This is the main entry point of the application. It is
# called when the script is run directly, i.e. `python main.py`.
# It creates an instance of the ContactBookApp class and
# calls its run method, which starts the app's event loop.
if __name__ == '__main__':
    ContactBookApp().run()

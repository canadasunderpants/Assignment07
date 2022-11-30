#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# jdenhaan, 2022-Nov-19, moved processing into functions
# jdenhaan, 2022-Nov-29, added error handling to script, changed file format to binary type
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
pcklFileName = 'CDInventory.dat' #binary data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """ Processor for data in runtime memory"""
    
    @staticmethod
    def DataDel():
        """
        Function which asks the user which row of data they would like to delete based on the ID. Looks for ID entered
        by searching the table row by row until it finds an equivalent ID. Deletes it from working memory. 

        Args: None
        Returns:None

        """
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('\nThat is not a valid ID')
            print(e)
        except Exception as e:
            print('General Error')
            print(e)
        finally:
            intRowNr = -1
            blnCDRemoved = False
            for row in lstTbl:
                intRowNr += 1
                if row['ID'] == intIDDel:
                    del lstTbl[intRowNr]
                    blnCDRemoved = True
                    break
                if blnCDRemoved:
                    print('The CD was removed')
                else:
                    print('Could not find this CD!')
    @staticmethod
    def DataAdd (ID, Title, Artist, table):
        """

        Function that asks user for input in the form of ID, Title and Artist. 4th arguement is the table that data 
        will be added to once entered. 

        Parameters
        ----------
        ID, Title, Artist: dictionary elements
        table: storage variable for rows of dicionary elements
        
        Returns
        -------
        None.

        """
        dicRow = {'ID': ID, 'Title': Title, 'Artist': Artist}
        table.append(dicRow)
        IO.show_inventory(table)
        
        


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from a binary file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            Table: 
        """
        #table.clear()  # this clears existing data and allows to load data from file
        try:
            with open (file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
                
        except FileNotFoundError as e:
            print('that file does not exist')
            print(e)
            print('Let me create that file for you!')
            fileNew = open(file_name, 'wb')
            fileNew.close()
            print('The file {} has now been created'.format(file_name))
            
        finally:
            return table
            print(table)
        

    @staticmethod
    def write_file(file_name, table):
        """
        writes data entered by user to a binary file for permanent storage

        Args:
            file_name (string): name of file to write data to
            table (list of dict):2D data structure (list of dicts) that holds the data during runtime,
            holds data to be written to file

        Returns
            None.

        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def DataInput():
        """
        function to ask for user input, asks for an ID, CD title and an Artists, then writes 
        those to a dictionary (dicRow), then appends that dictionary to lstTbl in working
        memory

        Returns
        -------
       intID, strTitle, strArtist - will be used directly in saving to lstTbl variable

        """
         
        try:
            strID = input('Enter ID: ').strip()
            strTitle = input('What is the CD\'s title? ').strip()
            strArtist = input('What is the Artist\'s name? ').strip()
            intID = int(strID)
        
        except ValueError as e:
            print('\nERROR! ID must be an integer.')
            print(e)
            print()
        finally:
            return intID, strTitle, strArtist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(pcklFileName)
print(lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            try:
                print('reloading...')
                lstTbl = FileProcessor.read_file(pcklFileName)
                IO.show_inventory(lstTbl)
            except:
                continue
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        try:
            strID, strTitle, strArtist = IO.DataInput()
        except:
            continue
        # 3.3.2 Add item to the table
        DataProcessor.DataAdd(strID, strArtist, strTitle, lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # 3.5.2 search thru table and delete CD
        try:
            DataProcessor.DataDel()
        except:
            continue
        #3.5.3 display updated inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file('CDInventory.pickle', lstTbl)
        if strYesNo == 'n':    
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')





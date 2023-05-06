from DataFrameManager import *
from GUI import *

def main():
    print('App initialized')
    try:
        # Importing csv and processing dataframe
        dfm = DataFrameManager()
        
        # Tkinter GUI
        print('Building GUI...')
        root = tk.Tk()
        
        # Functions for closing app
        def close(event):
            root.destroy()
            plt.close('all')
        def close_window():
            root.destroy()
            plt.close('all')
        
        root.protocol("WM_DELETE_WINDOW", close_window)
        root.bind('<Escape>',close)
        root.title('Olympic Women\'s Data Visualization')

        # Running main loop
        app = GUI(root, dfm)
        root.mainloop()
    except:
        print('Error occured')


if __name__ == '__main__':
    main()

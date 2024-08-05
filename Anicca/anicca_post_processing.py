import os
import pandas as pd
import matplotlib.pyplot as plt
import re

class GraphPlotter:
    def __init__(self, base_dir):
        """
        Initialize the GraphPlotter class with the given base directory.

        Parameters:
        base_dir (str): The base directory where the scenarios and datasets are located.

        Attributes:
        base_dir (str): The base directory.
        selected_scenario_dirs (list): A list to store the selected scenario directories.
        dataset_dirs (list): A list to store the dataset directories for each selected scenario.
        graphs_dir (str): The directory where the generated graphs will be saved.
        selected_sheets (list): A list to store the selected sheets (regions) to analyze.
        graph_mode (str): The mode of graph generation, either "auto" or "manual".
        translation_dict_y (dict): A dictionary to translate y-axis labels.
        translation_dict_legend (dict): A dictionary to translate legend labels.
        color_dict (dict): A dictionary to map variables to colors.
        line_styles (list): A list of line styles for different scenarios.
        figsize (tuple): The size of the figure for generated graphs.
        """
        self.base_dir = base_dir
        self.selected_scenario_dirs = []
        self.dataset_dirs = []
        self.graphs_dir = ""
        self.selected_sheets = []
        self.graph_mode = "auto"
        self.translation_dict_y = {
            "92.0 (tons)": "tHM",
            "93.0 (tons)": "tHM",
            "94.0 (tons)": "tHM",
            "95.0 (tons)": "tHM",
            "96.0 (tons)": "tHM",
            "Fission_product (tons)": "tHM",
            "minor_actinide (tons)": "tHM",
            "Uox_45 (tons)": "Mass (t)",
            "Uox_45_spent (tons)": "Mass (t)",
            "Depu (tons)": "Mass (t)",
            "Nat (tons)": "Mass (t)"
        }
        self.translation_dict_legend = {
            "92.0 (tons)": "Uranium",
            "93.0 (tons)": "Neptunium",
            "94.0 (tons)": "Plutonium",
            "95.0 (tons)": "Americium",
            "96.0 (tons)": "Curium",
            "Fission_product (tons)": "Fission Products",
            "minor_actinide (tons)": "Minor Actinides",
            "Uox_45 (tons)": "UOX 45",
            "Uox_45_spent (tons)": "UOX 45 SPENT",
            "Depu (tons)": "Depleted Uranium",
            "Nat (tons)": "Natural Uranium"
        }
        self.color_dict = {
            "92.0 (tons)": "#BC3D3D",
            "93.0 (tons)": "#4268BE",
            "94.0 (tons)": "#4268BE",
            "95.0 (tons)": "#8A4EE0",
            "96.0 (tons)": "#67DC80",
            "Fission_product (tons)": "#4268BE",
            "minor_actinide (tons)": "#BC3D3D",
            "Uox_45 (tons)": "black",
            "Uox_45_spent (tons)": "black"
        }
        self.line_styles = ['-', '--', '-.', ':']
        self.figsize = (15, 10)

    def create_directory(self, directory_path):
        """
        Creates a directory at the specified path if it does not exist.

        Parameters:
        directory_path (str): The path where the directory will be created.

        Returns:
        None
        """
        os.makedirs(directory_path, exist_ok=True)

    def list_directories(self, directory_path):
        """
        List all directories within a specified directory, excluding the "graphs" directory.

        Parameters:
        directory_path (str): The path of the directory to list directories from.

        Returns:
        list: A list of directory names within the specified directory, excluding "graphs".
        """
        return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d)) and d != "graphs"]

    def list_files(self, directory_path, extension='.xlsx'):
        """
        List all files within a specified directory with a given extension.

        Parameters:
        directory_path (str): The path of the directory to list files from.
        extension (str): The file extension to filter files by. Default is '.xlsx'.

        Returns:
        list: A list of file names within the specified directory that match the given extension.
        """
        return [f for f in os.listdir(directory_path) if f.endswith(extension)]

    def select_option(self, prompt, options):
        """
        This function displays a list of options to the user and prompts them to select one.

        Parameters:
        prompt (str): The message to display before displaying the options.
        options (list): A list of strings representing the options to display.

        Returns:
        int: The index of the selected option (0-based).
        """
        print(prompt)
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")
        return int(input("Select an option: ")) - 1

    def select_scenarios(self):
        """
        Selects scenarios for comparison by prompting the user to input the number of scenarios and their indices.
        Updates the attributes `selected_scenario_dirs`, `dataset_dirs`, and `graphs_dir` accordingly.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        None
        """
        scenarios = self.list_directories(self.base_dir)
        num_scenarios = int(input(f"How many scenarios do you want to compare (1-{len(scenarios)}): "))
        print("Select scenarios to compare (e.g., 1,3,5):")
        for i, scenario in enumerate(scenarios):
            print(f"{i + 1}. {scenario}")
        selected_indices = list(map(int, input("Enter scenario numbers: ").split(',')))
        self.selected_scenario_dirs = [os.path.join(self.base_dir, scenarios[i - 1]) for i in selected_indices]
        self.dataset_dirs = [os.path.join(scenario, "output") for scenario in self.selected_scenario_dirs]
        self.graphs_dir = os.path.join(self.base_dir, "graphs")
        self.create_directory(self.graphs_dir)

    def select_graph_mode(self):
        """
        This function prompts the user to select a graph mode (automatic or manual) and updates the `graph_mode` attribute accordingly.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        None
        """
        print("Select the graph mode:")
        print("1. Automatic graph")
        print("2. Manual graph")
        mode = int(input("Select an option (1 or 2): "))
        self.graph_mode = "auto" if mode == 1 else "manual"

    def select_graph_type(self):
        """
        This function prompts the user to select a graph type (normal or subplot) and, if subplot is selected,
        prompts the user to select the subplot dimensions.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        tuple: A tuple containing two elements:
            1. An integer representing the selected graph type (1 for normal, 2 for subplot).
            2. A tuple representing the subplot dimensions if subplot is selected, otherwise None.
        """
        print("Select the type of graph:")
        print("1. Normal graph")
        print("2. Subplot")
        graph_type = int(input("Select an option (1 or 2): "))
        if graph_type == 2:
            print("Select subplot type:")
            print("1. 1x2")
            print("2. 1x3")
            print("3. 2x1")
            print("4. 2x2")
            print("5. 2x3")
            print("6. 3x1")
            print("7. 3x2")
            subplot_type = int(input("Select an option (1-7): "))
            subplot_map = {
                1: (1, 2), 2: (1, 3), 3: (2, 1),
                4: (2, 2), 5: (2, 3), 6: (3, 1),
                7: (3, 2)
            }
            return graph_type, subplot_map[subplot_type]
        return graph_type, None

    def select_figsize(self):
        """
        This function prompts the user to input the width and height for the figure size.
        The entered values are then used to update the `figsize` attribute of the GraphPlotter instance.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        None

        Side Effects:
        Updates the `figsize` attribute of the GraphPlotter instance.
        """
        width = float(input("Enter the width of the figure: "))
        height = float(input("Enter the height of the figure: "))
        self.figsize = (width, height)

    def select_sheets(self):
        """
        Selects sheets (regions) to analyze from the dataset directories.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        None

        Side Effects:
        Updates the `selected_sheets` attribute of the GraphPlotter instance.
        """
        files = self.list_files(self.dataset_dirs[0])
        sheet_options = []
        for file in files:
            file_path = os.path.join(self.dataset_dirs[0], file)
            excel_file = pd.ExcelFile(file_path)
            for sheet in excel_file.sheet_names:
                sheet_options.append(f"{file} - {sheet}")

        print("Select the sheets (regions) to analyze (e.g., 1,3,5):")
        for i, option in enumerate(sheet_options):
            print(f"{i + 1}. {option}")
        selected_indices = list(map(int, input("Enter sheet numbers: ").split(',')))
        selected_options = [sheet_options[i - 1] for i in selected_indices]
        self.selected_sheets = [(option.split(" - ")[0], option.split(" - ")[1]) for option in selected_options]

    def select_variables(self):
        """
        This function prompts the user to select variables from the dataset.
        It reads the first dataset file and sheet, lists all available variables,
        and then prompts the user to enter variable numbers.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.

        Returns:
        list: A list of selected variables. Each variable is represented as a string.

        Side Effects:
        Prints available variables and prompts the user for input.
        """
        file_path = os.path.join(self.dataset_dirs[0], self.selected_sheets[0][0])
        df = pd.read_excel(file_path, sheet_name=self.selected_sheets[0][1])
        all_variables = df.columns.tolist()

        print("Available variables:")
        for i, var in enumerate(all_variables):
            print(f"{i + 1}. {var}")

        input_str = input("Enter variable numbers (e.g., 1,4),(3,7),14: ")
        variable_groups = re.findall(r'\((.*?)\)|(\d+)', input_str)
        selected_vars = []
        for group in variable_groups:
            if group[0]:
                selected_vars.append([all_variables[int(x) - 1] for x in group[0].split(',')])
            else:
                selected_vars.append([all_variables[int(group[1]) - 1]])
        return selected_vars

    def plot_graphs(self, graph_type, subplot_dims, selected_vars):
        """
        Plots graphs based on the selected graph type, subplot dimensions, and selected variables.

        Parameters:
        self (GraphPlotter): The instance of the GraphPlotter class.
        graph_type (int): An integer representing the type of graph to be plotted. It can be either 1 (normal graph) or 2 (subplot).
        subplot_dims (tuple): A tuple representing the dimensions of the subplot. It is only used when `graph_type` is 2.
        selected_vars (list): A list of selected variables to be plotted on the graphs.

        Returns:
        None
        """
        for selected_file, selected_sheet in self.selected_sheets:
            if graph_type == 1:
                for var_group in selected_vars:
                    plt.figure(figsize=self.figsize)
                    for idx, dataset_dir in enumerate(self.dataset_dirs):
                        scenario_name = f"Scenario {idx + 1}"
                        file_path = os.path.join(dataset_dir, selected_file)
                        df = pd.read_excel(file_path, sheet_name=selected_sheet)
                        for var in var_group:
                            if var in df.columns:
                                x_values = df.iloc[:, 0]
                                y_values = df[var]
                                legend_label = f'{self.translation_dict_legend.get(var, var)} - {scenario_name}'
                                color = self.color_dict.get(var, 'black')
                                line_style = self.line_styles[idx % len(self.line_styles)]
                                plt.plot(x_values, y_values, label=legend_label, color=color, linestyle=line_style)
                    plt.legend(fontsize=14)
                    plt.xlabel('Year', fontsize=15)
                    plt.ylabel(self.translation_dict_y.get(var_group[0], var_group[0]), fontsize=15)
                    plt.xlim(2000, 2100)
                    plt.ylim(bottom=0)
                    plt.grid(True)
                    variable_dir = os.path.join(self.graphs_dir, selected_file.replace(".xlsx", ""))
                    self.create_directory(variable_dir)
                    graph_path = os.path.join(variable_dir, f'{"_".join(var_group)}_{selected_sheet}.png')
                    if self.graph_mode == "auto":
                        plt.savefig(graph_path)
                        plt.close()
                    else:
                        plt.show()
            elif graph_type == 2:
                fig, axes = plt.subplots(subplot_dims[0], subplot_dims[1], figsize=self.figsize)
                axes = axes.flatten()
                for i, var_group in enumerate(selected_vars):
                    ax = axes[i]
                    for idx, dataset_dir in enumerate(self.dataset_dirs):
                        scenario_name = f"Scenario {idx + 1}"
                        file_path = os.path.join(dataset_dir, selected_file)
                        df = pd.read_excel(file_path, sheet_name=selected_sheet)
                        for var in var_group:
                            if var in df.columns:
                                x_values = df.iloc[:, 0]
                                y_values = df[var]
                                legend_label = f'{self.translation_dict_legend.get(var, var)} - {scenario_name}'
                                color = self.color_dict.get(var, 'black')
                                line_style = self.line_styles[idx % len(self.line_styles)]
                                ax.plot(x_values, y_values, label=legend_label, color=color, linestyle=line_style)
                    ax.legend(fontsize=14)
                    ax.set_xlabel('Year', fontsize=15)
                    ax.set_ylabel(self.translation_dict_y.get(var_group[0], var_group[0]), fontsize=15)
                    ax.set_xlim(2000, 2100)
                    ax.set_ylim(bottom=0)
                    ax.grid(True)
                plt.tight_layout()
                variable_dir = os.path.join(self.graphs_dir, selected_file.replace(".xlsx", ""))
                self.create_directory(variable_dir)
                graph_path = os.path.join(variable_dir, f'subplot_graph_{selected_sheet}.png')
                if self.graph_mode == "auto":
                    plt.savefig(graph_path)
                    plt.close()
                else:
                    plt.show()

class TableCreator:
    def __init__(self, base_dir):
        """
        Initialize the TableCreator class with the given base directory.

        Parameters:
        base_dir (str): The base directory where the scenarios and datasets are located.

        Attributes:
        base_dir (str): The base directory where the scenarios and datasets are located.
        selected_scenario_dirs (list): A list to store the selected scenario directories.
        dataset_dirs (list): A list to store the dataset directories corresponding to the selected scenarios.
        tables_dir (str): The directory where the comparison tables will be saved.
        translation_dict (dict): A dictionary to map variable names to their translated names.
        years_of_interest (list): A list of years for which data will be extracted and compared.
        region_keywords (dict): A dictionary to map region keywords to their full names.
        """
        self.base_dir = base_dir
        self.selected_scenario_dirs = []
        self.dataset_dirs = []
        self.tables_dir = ""
        self.translation_dict = {
            "92.0 (tons)": "Uranium (tHM)",
            "93.0 (tons)": "Neptunium (tHM)",
            "94.0 (tons)": "Plutonium (tHM)",
            "95.0 (tons)": "Americium (tHM)",
            "96.0 (tons)": "Curium (tHM)",
            "Fission_product (tons)": "Fission Products (tHM)",
            "minor_actinide (tons)": "Minor Actinides (tHM)",
            "Uox_45 (tons)": "UOX 45 (tons)",
            "Uox_45_spent (tons)": "UOX 45 SPENT (tons)",
            "SWU": "SWU (kSWU)",
            "Net_power": "Net Power (MWe)"
        }
        self.years_of_interest = [2022, 2030, 2050, 2100]
        self.region_keywords = {
            "WEST_EUROPE_COP": "West Europe COP",
            "WEST_EUROPE": "West Europe",
            "EAST_EUROPE_COP": "East Europe COP",
            "EAST_EUROPE": "East Europe",
            "NORTH_AMERICA_COP": "North America COP",
            "NORTH_AMERICA": "North America",
            "RUSSIA": "Russia",
            "ASIA_COP": "Asia COP",
            "ASIA": "Asia"
        }

    def create_directory(self, directory_path):
        """
        Creates a directory at the specified path if it does not exist.

        Parameters:
        directory_path (str): The path where the directory will be created.

        Returns:
        None
        """
        os.makedirs(directory_path, exist_ok=True)

    def list_directories(self, directory_path):
        """
        List all directories within a specified directory, excluding the "tables" directory.

        Parameters:
        directory_path (str): The path of the directory to list subdirectories from.

        Returns:
        list: A list of directory names within the specified directory, excluding "tables".
        """
        return [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d)) and d != "tables"]

    def list_files(self, directory_path, extension='.xlsx'):
        """
        List all files within a specified directory with a given extension.

        Parameters:
        directory_path (str): The path of the directory to list files from.
        extension (str): The file extension to filter files by. Default is '.xlsx'.

        Returns:
        list: A list of file names within the specified directory that match the given extension.
        """
        return [f for f in os.listdir(directory_path) if f.endswith(extension)]

    def map_sheet_to_region(self, sheet_name):
        """
        Map a sheet name to its corresponding region based on predefined keywords.

        Parameters:
        sheet_name (str): The name of the sheet to map.

        Returns:
        str: The corresponding region for the given sheet name. If no match is found, returns None.
        """
        for keyword, region in self.region_keywords.items():
            if keyword in sheet_name:
                return region
        return None

    def select_scenarios(self):
        """
        Select scenarios for comparison based on user input.

        This function prompts the user to select a number of scenarios for comparison.
        It lists the available scenarios, asks the user to input their selection,
        and then creates the necessary directories for the selected scenarios.

        Parameters:
        self (TableCreator): The instance of the TableCreator class.

        Returns:
        None
        """
        scenarios = self.list_directories(self.base_dir)
        num_scenarios = int(input(f"How many scenarios do you want to compare (1-{len(scenarios)}): "))
        print("Select scenarios to compare (e.g., 1,3,5):")
        for i, scenario in enumerate(scenarios):
            print(f"{i + 1}. {scenario}")
        selected_indices = list(map(int, input("Enter scenario numbers: ").split(',')))
        self.selected_scenario_dirs = [os.path.join(self.base_dir, scenarios[i - 1]) for i in selected_indices]
        self.dataset_dirs = [os.path.join(scenario, "output") for scenario in self.selected_scenario_dirs]
        self.tables_dir = os.path.join(self.base_dir, "tables")
        self.create_directory(self.tables_dir)

    def list_variables(self):
        """
        This function lists all available variables from the dataset directories.
        It reads each Excel file in the dataset directories, extracts the sheet names,
        and then reads the column names from each sheet.
        The function then maps each unique file-column combination to a variable option.
        The variable options are sorted and printed with their corresponding numbers.

        Parameters:
        self (TableCreator): The instance of the TableCreator class.

        Returns:
        list: A list of all available variable options.
        """
        variable_options = {}
        for dataset_dir in self.dataset_dirs:
            files = self.list_files(dataset_dir)
            for file in files:
                file_path = os.path.join(dataset_dir, file)
                excel_file = pd.ExcelFile(file_path)
                for sheet in excel_file.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    for column in df.columns:
                        key = f"{file} - {column}"
                        if key not in variable_options:
                            variable_options[key] = column
        variable_options = dict(sorted(variable_options.items()))

        current_file = None
        counter = 1
        for key in variable_options.keys():
            file, variable = key.split(' - ')
            if file != current_file:
                current_file = file
                print(f"\033[91m{file}\033[0m") 
            print(f"{counter}. {variable}")
            counter += 1

        return list(variable_options.keys())

    def select_variables(self):
        """
        This function prompts the user to select variables for comparison.
        It first lists all available variables using the list_variables() method.
        Then, it takes user input in the format of variable numbers (e.g., 1,4),(3,7),14.
        The input is parsed and grouped into individual variable selections.
        Finally, it returns a list of selected variables.

        Parameters:
        self (TableCreator): The instance of the TableCreator class.

        Returns:
        list: A list of selected variables. Each variable is represented as a string in the format "file - column".
        """
        all_variables = self.list_variables()

        input_str = input("Enter variable numbers (e.g., 1,4),(3,7),14: ")
        variable_groups = re.findall(r'\((.*?)\)|(\d+)', input_str)
        selected_vars = []
        for group in variable_groups:
            if group[0]:
                selected_vars.append([all_variables[int(x) - 1] for x in group[0].split(',')])
            else:
                selected_vars.append([all_variables[int(group[1]) - 1]])
        return selected_vars

    def create_tables(self, num_tables, all_selected_vars):
        """
        This function creates comparison tables for different scenarios and regions.
        It reads data from Excel files, filters the data based on years of interest,
        and calculates percentage increases for each variable.
        The function then writes the comparison tables to an Excel file.

        Parameters:
        self (TableCreator): The instance of the TableCreator class.
        num_tables (int): The number of tables to create.
        all_selected_vars (list): A list of selected variables for each table.

        Returns:
        None
        """
        with pd.ExcelWriter(os.path.join(self.tables_dir, 'comparison_tables.xlsx')) as writer:
            for scenario_idx, dataset_dir in enumerate(self.dataset_dirs):
                scenario_name = f"Scenario_{scenario_idx + 1}"
                for region in self.region_keywords.values():
                    start_row = 0
                    for table_num in range(num_tables):
                        selected_vars = all_selected_vars[table_num]
                        combined_df = pd.DataFrame()
                        for var_group in selected_vars:
                            for var in var_group:
                                file_var, column = var.split(' - ')
                                variable_added = False
                                new_row = {'Variable': self.translation_dict.get(column, column), 'Region': region}
                                prev_value = None
                                files = self.list_files(dataset_dir)
                                for file in files:
                                    if file == file_var:
                                        file_path = os.path.join(dataset_dir, file)
                                        excel_file = pd.ExcelFile(file_path)
                                        for sheet in excel_file.sheet_names:
                                            if self.map_sheet_to_region(sheet) == region:
                                                df = pd.read_excel(file_path, sheet_name=sheet)
                                                filtered_df = df[df.iloc[:, 0].isin(self.years_of_interest)]
                                                for year in self.years_of_interest:
                                                    value = filtered_df[filtered_df.iloc[:, 0] == year][column].values[0] if column in filtered_df.columns else None
                                                    if value is not None:
                                                        value = int(value)
                                                    new_row[year] = value
                                                    if year == self.years_of_interest[0]:
                                                        new_row[f'{year} %'] = "100%"
                                                        prev_value = value
                                                    else:
                                                        if prev_value is not None and value is not None and prev_value != 0:
                                                            percentage_increase = ((value - prev_value) / prev_value) * 100
                                                            new_row[f'{year} %'] = f"{int(percentage_increase)}%"
                                                        else:
                                                            new_row[f'{year} %'] = "0%"
                                                        prev_value = value
                                                variable_added = True
                                if variable_added:
                                    combined_df = pd.concat([combined_df, pd.DataFrame([new_row])], ignore_index=True)
                                    if column == 'Net_power':
                                        reactor_row = new_row.copy()
                                        reactor_row['Variable'] = 'Nuclear Reactors (u)'
                                        prev_value_reactors = None
                                        for year in self.years_of_interest:
                                            if new_row[year] is not None:
                                                reactor_row[year] = int(new_row[year] / 1000)
                                                if year == self.years_of_interest[0]:
                                                    reactor_row[f'{year} %'] = "100%"
                                                    prev_value_reactors = reactor_row[year]
                                                else:
                                                    if prev_value_reactors is not None and prev_value_reactors != 0:
                                                        percentage_increase_reactors = ((reactor_row[year] - prev_value_reactors) / prev_value_reactors) * 100
                                                        reactor_row[f'{year} %'] = f"{int(percentage_increase_reactors)}%"
                                                    else:
                                                        reactor_row[f'{year} %'] = "0%"
                                                    prev_value_reactors = reactor_row[year]
                                        combined_df = pd.concat([combined_df, pd.DataFrame([reactor_row])], ignore_index=True)
                        if not combined_df.empty:
                            combined_df.to_excel(writer, sheet_name=f"{scenario_name}_{region}", index=False, startrow=start_row)
                            start_row += len(combined_df) + 3

def main():
    print("Select the mode:")
    print("1. Graph Plotting")
    print("2. Table Creation")
    mode = int(input("Select an option (1 or 2): "))
    
    base_dir = os.path.dirname(__file__)
    
    if mode == 1:
        plotter = GraphPlotter(base_dir)
        plotter.select_scenarios()
        plotter.select_graph_mode()
        plotter.select_sheets()
        graph_type, subplot_dims = plotter.select_graph_type()
        plotter.select_figsize()
        selected_vars = plotter.select_variables()
        plotter.plot_graphs(graph_type, subplot_dims, selected_vars)
    elif mode == 2:
        creator = TableCreator(base_dir)
        creator.select_scenarios()
        num_tables = int(input("Enter the number of tables you want to create: "))
        all_selected_vars = []
        for i in range(num_tables):
            print(f"\nSelecting variables for table {i + 1}")
            selected_vars = creator.select_variables()
            all_selected_vars.append(selected_vars)
        creator.create_tables(num_tables, all_selected_vars)
    else:
        print("Invalid option selected. Please restart the program.")

if __name__ == "__main__":
    main()

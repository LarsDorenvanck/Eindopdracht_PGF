import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))

def read_stored_reports():
    """
    Read and display stored reports from the 'reports' folder.

    This function allows the user to select and read a report from the available
    text files in the 'reports' folder. It provides a menu interface for report selection.

    Returns:
        str or None: The content of the selected report as a string, or None if no report is selected or if an error occurs.
    """
    report_folder = os.path.join(current_dir, 'reports')
    if not os.path.exists(report_folder):
        print("No reports folder found.")
        return None

    reports = [f for f in os.listdir(report_folder) if f.endswith('.txt')]
    
    if not reports:
        print("No reports found in the reports folder.")
        return None

    while True:
        print("Available reports:")
        for i, report in enumerate(reports, 1):
            print(f"{i}. {report}")
        print("q. Quit")

        choice = input("Enter the number of the report you want to read (or 'q' to quit): ")
        if choice.lower() == 'q':
            return None

        try:
            report_index = int(choice) - 1
            if 0 <= report_index < len(reports):
                report_path = os.path.join(report_folder, reports[report_index])
                if not os.path.exists(report_path):
                    print(f"Report '{reports[report_index]}' not found. It may have been deleted.")
                    return None
                with open(report_path, 'r') as f:
                    return f.read()
            else:
                print("Invalid report number.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")

if __name__ == "__main__":
    read_stored_reports()
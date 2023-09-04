import re
import pandas as pd

from typing import Tuple




def get_semester_code(obj, course_title=None):
    """Gets and return the semester of the result as an
    integer from either a dataframe object or the course code as a string."""
    if isinstance(obj, pd.DataFrame):
        course = obj.index[0]
        course_title = obj.loc[course]['title']
    elif isinstance(obj, str):  # i.e. if the `obj` is the course code from the form
        course = obj
    if "SWEP" in course_title:
        return 3
    last_dgt = int(course[-1])
    return 2 if last_dgt % 2 == 0 else 1


def parse_result_html(file) -> Tuple:
    """
    This function parses the HTML file containing the results of a Student (esp. University of Ilorin)
    into a pandas DataFrame and creates a Semester object for each individual semester contained in the result.
    Ensure the HTML files are stored in a folder named 'results' and the filenames are named in ascending order 
    according to their corresponding years to enable the function locate it.
    :return: List[pandas.DataFrame]
    """
    grade = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
        }
    # the original names of the variables
    # matric, name, fac, dept, level = pd.read_html(file)[0][1]
    _, _, fac, dept, level = pd.read_html(file)[0][1]
    
    # extracting the session id
    # decoding the `file` object which is an io.BytesIO object
    
    try:
        content = file.getvalue().decode()
    except UnicodeDecodeError:
        content = file.getvalue().decode(encoding='ISO-8859-1')
    session = re.search('\d\d\d\d/\d\d\d\d', content).group()

    dfs = pd.read_html(file, header=1, index_col=1)
    for df in dfs[1:]:
        df.drop(columns=['Unnamed: 9', 'S/No.'], index='Total', inplace=True)
        df['Gradient'] = pd.Series(
            [df.loc[f]['Unit'] * grade.get(df.loc[f]['Grade'], 0) for f in df.index],
            index=df.index,
            dtype='int8'
            )

    return dfs[1:], session, level, fac, dept

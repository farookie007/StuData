import re
import json
import pandas as pd

from results.models import (
    Level,
    Semester,
    Session,
    SemesterResult,
    Course,
)
from accounts.models import CustomUser as User

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


def obj_to_dict(obj, fields):
    """
    Function for making a dictionary representation of an object `obj`'s fields
    as a key-value pair.
    Params:
        obj: the object to be turned into dictionary
        fields: List: the list of fields to be included in the dictionary
    Return:
        the dictionary
    """
    field_values = [obj.serializable_value(f) for f in fields]
    return dict(zip(fields, field_values))

def get_obj_fields(obj):
    return [f.name for f in obj._meta.fields]


def write_to_json(filename, payload, indent=4):
    with open(filename + '.json', 'w') as fp:
        json.dump(payload, fp, indent=indent)


def jsonnify_model(model, preffered_fields=None, indent=4):
    if preffered_fields is None:
        preffered_fields = get_obj_fields(model)
    objects = model.objects.all()
    payload = [obj_to_dict(obj, preffered_fields) for obj in objects]
    write_to_json(model.__name__, payload, indent=indent)


def get_payload(filename):
    with open(filename + '.json', 'r') as fp:
        payload = json.load(fp)
    return payload


def deserialize_ForeignKeys(payload):
    obj_map = {
        'level': Level,
        'session': Session,
        'result': SemesterResult,
        'semester': Semester,
        'course': Course,
    }
    for load in payload:
        for k in load.keys():
            obj = obj_map.get(k)
            if obj is not None:
                load[k] = obj.objects.filter(id=load[k]).first()

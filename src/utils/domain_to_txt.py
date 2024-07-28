import datetime

def write_fields_to_txt(models):
    """
    Documents the field names and their types for each Pydantic model and writes them to a text file for frontend usage.

    This function takes a list of Pydantic model classes, extracts the field names and their corresponding types,
    and writes this information to a file named 'output.txt'. Each model's fields are listed under the model's name,
    formatted as TypeScript interfaces. Additionally, TSLint and ESLint disable comments are included for compatibility.

    Args:
        models (list): A list of Pydantic model classes to process.

    The output file format:
    Use domains in models for frontend:

    /* tslint:disable */
    /* eslint-disable */

    export interface ModelName {
      field_name: field_type;
      ...
    }

    Example:
        Use domains in models for frontend:

        /* tslint:disable */
        /* eslint-disable */

        export interface Blog {
          _id: string;
          naslov: string;
          kategorija: string;
          ...
        }

        export interface Experiences {
          _id: string;
          title: string;
          stack: string;
          ...
        }
    """
    with open('output.txt', 'w') as f:
        f.write('Use domains in models for frontend:\n\n')
        for model in models:
            f.write(f'/* tslint:disable */ \n/* eslint-disable */ \n\n')
            model_name = model.__name__  # Get the name of the model class
            f.write(f'export interface {model_name} {{\n')  # Write the model name as a TypeScript interface
            for field_name, field_info in model.__fields__.items():
                if field_name == 'id':
                    f.write(" '_id'?: string;\n")  # Write _id field with type 'str'
                    continue
                field_type = field_info.type_  # Get the type of the field

                # Map field types to TypeScript types
                if field_type is bool:
                    type_name = 'boolean;'
                elif field_type is datetime.datetime:
                    type_name = 'string;'
                elif field_type is str:
                    type_name = 'string;'
                else:
                    # Convert the type to a readable string format
                    type_name = str(field_type).replace("<class '", '').replace("'>", '')

                f.write(f'  {field_name}: {type_name}\n')  # Write the field name and type to the file
            f.write('}\n\n')  # Close the interface and add a newline for separation between models

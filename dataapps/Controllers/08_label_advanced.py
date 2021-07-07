from shapelets import init_session
from shapelets.dsl import DataApp
import shapelets.dsl.dsl_op as dsl_op


# Custom function
# Returns a string message which tells if x is greater than y
def greater_than(x: int, y: int) -> str:
    return f"{x} is greater than {y}" if x > y else f"{x} is less or equals than {y}"


# Init session
client = init_session("admin", "admin")

# Register custom function
client.register_custom_function(greater_than)

# Creating DataApp
app = DataApp(name="08_label_advanced", description="This DataApp renders a label after execution result")

# Create inputs number
x = app.number(name="x", value_type=int)
y = app.number(name="y", value_type=int)

# Create button
button = app.button(text="Execute")

# Compose graph
result = dsl_op.greater_than(x, y)

# Handle click execute graph
button.on_click([result])

# Place result in label
label = app.label(result)

# Place widgets into the DataApp
app.place(x)
app.place(y)
app.place(button)
app.place(label)

# Register the DataApp
client.register_data_app(app)

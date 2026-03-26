from mcp.server.fastmcp import FastMCP
from print import (
    current_date as get_current_date,
    current_month as get_current_month,
    current_time as get_current_time,
    current_time_only as get_current_time_only,
    current_year as get_current_year,
)

mcp = FastMCP("datetime-tools")

@mcp.tool()
def current_time():
    return get_current_time()


@mcp.tool()
def current_date():
    return get_current_date()


@mcp.tool()
def current_time_only():
    return get_current_time_only()


@mcp.tool()
def current_month():
    return get_current_month()


@mcp.tool()
def current_year():
    return get_current_year()





if __name__ == "__main__":
    mcp.run()

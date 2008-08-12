from pkg_resources import resource_filename
from turbogears import widgets
from turbogears.widgets import PaginateDataGrid
import fpformat

# datagrids
# find 'static' directory in package 'ffbstatssa'
static_dir = resource_filename('ffbstatssa', 'static')
# register directory under name 'ffbstatssa'
widgets.register_static_directory('ffbstatssa', static_dir)

# datagrid for index page
teams_datagrid = PaginateDataGrid(
    name='team_list', template="ffbstatssa.templates.datagrid",
    fields = [
        PaginateDataGrid.Column('name',
                                'name',
                                'Name',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('owner',
                                'owner',
                                'Owner',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('total_points',
                                'total_points',
                                'P',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('total_possible_points',
                                'total_possible_points',
                                'OP',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('efficiency',
                                lambda teams: (
                                    "".join([str(fpformat.fix(
                                        (teams.efficiency * 100), 2)), "%"])), 
                                'Efficiency',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('wins',
                                'wins',
                                'W',
                                options=dict(sortable=True)),
        PaginateDataGrid.Column('losses',
                                'losses',
                                'L',
                                options=dict(sortable=True)),
    ]
)

# change the css file for the widgets
teams_datagrid.css = [widgets.CSSLink('ffbstatssa', 'css/team_dg.css')]
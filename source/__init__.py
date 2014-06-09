# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# make all SWIG objects available at top level
from .lib import *

# define some higher level Python classes
class Context(object):
    """Context helper class.

    Wraps all gp_*(..., context) function calls. For example
        gp_camera_autodetect(list, context)
    becomes
        Context.camera_autodetect(list)

    The context attribute stores the low-level GPContext object
    created by the helper class.
    
    """
    def __init__(self, use_python_logging=True):
        """Constructor.

        Arguments:
        use_python_logging -- should errors be logged via Python's
        logging package.

        """
        if use_python_logging:
            check_result(lib.use_python_logging())
        self.context = gp_context_new()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __getattr__(self, name):
        self._next_call = getattr(lib, 'gp_%s' % name)
        return self._call

    def _call(self, *arg):
        return check_result(
            (self._next_call)(*(arg + (self.context,))))

    def cleanup(self):
        """Release resources allocated during object creation."""
        gp_context_unref(self.context)

class Camera(object):
    """Camera helper class.

    Wraps all gp_camera_*(camera, ..., context) function calls. For
    example
        gp_camera_folder_list_files(camera, folder, list, context)
    becomes
        Camera.list_files(folder, list)

    The camera attribute stores the low-level Camera object created by the
    helper class.
    
    """
    def __init__(self, context):
        """Constructor.

        Arguments:
        context -- a GPContext object.

        """
        self.context = context
        self.camera = check_result(gp_camera_new())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __getattr__(self, name):
        self._next_call = getattr(lib, 'gp_camera_%s' % name)
        return self._call

    def _call(self, *arg):
        return check_result(
            (self._next_call)(self.camera, *(arg + (self.context,))))

    def cleanup(self):
        """Release resources allocated during object creation."""
        check_result(gp_camera_unref(self.camera))

class CameraWidget(object):
    """CameraWidget helper class.

    Wraps all gp_widget_*(widget, ...) function calls. For example
        gp_widget_get_child(widget, child_number)
    becomes
        CameraWidget.get_child(child_number)

    The widget attribute stores the low-level CameraWidget object.
    
    """
    def __init__(self, widget):
        """Constructor.

        Arguments:
        widget -- a CameraWidget object.

        """
        self.widget = widget

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __getattr__(self, name):
        self._next_call = getattr(lib, 'gp_widget_%s' % name)
        return self._call

    def _call(self, *arg):
        return check_result((self._next_call)(self.widget, *arg))

    def cleanup(self):
        """Release resources allocated during object creation."""
        check_result(gp_widget_unref(self.widget))

class CameraList(object):
    """CameraList helper class.

    Wraps all gp_list_*(list, ...) function calls. For example
        gp_list_get_name(list, index)
    becomes
        CameraList.get_name(index)

    The list attribute stores the low-level CameraList object created
    by the helper class.
    
    """
    def __init__(self):
        self.list = check_result(gp_list_new())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

    def __getattr__(self, name):
        self._next_call = getattr(lib, 'gp_list_%s' % name)
        return self._call

    def _call(self, *arg):
        return check_result((self._next_call)(self.list, *arg))

    def cleanup(self):
        """Release resources allocated during object creation."""
        check_result(gp_list_unref(self.list))
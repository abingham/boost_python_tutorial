#include <boost/python.hpp>

namespace bp=boost::python;

struct Coordinate {
    Coordinate(long xin, long yin) : x(xin), y(yin) {}
    long x;
    long y;
};

struct Coordinate_to_tuple
{
    static PyObject* convert(const Coordinate& c)
        {
            return bp::incref<>(
                bp::make_tuple(c.x, c.y).ptr());
        }
};

struct Coordinate_from_tuple
{
    Coordinate_from_tuple()
        {
            bp::converter::registry::push_back(
                &convertible,
                &construct,
                bp::type_id<Coordinate>());
        }

    // Determine if obj_ptr can be converted in a Coordinate
    static void* convertible(PyObject* obj_ptr)
        {
            if (!PyTuple_Check(obj_ptr)) return 0;
            if (PyTuple_Size(obj_ptr) != 2) return 0;
            if (!PyNumber_Check(PyTuple_GetItem(obj_ptr, 0))) return 0;
            if (!PyNumber_Check(PyTuple_GetItem(obj_ptr, 1))) return 0;

            return obj_ptr;
        }



    // Convert obj_ptr into a Coordinate
    static void construct(
        PyObject* obj_ptr,
        bp::converter::rvalue_from_python_stage1_data* data)
        {
            // Extract integral values from tuple
            long x_coord = PyLong_AsLong(PyNumber_Long(PyTuple_GetItem(obj_ptr, 0)));
            long y_coord = PyLong_AsLong(PyNumber_Long(PyTuple_GetItem(obj_ptr, 1)));

            // Grab pointer to memory into which to construct the new Coordinate
            void* storage = (
                (bp::converter::rvalue_from_python_storage<Coordinate>*)
                data)->storage.bytes;

            // in-place construct the new Coordinate using the character data
            // extraced from the python object
            new (storage) Coordinate(x_coord, y_coord);

            // Stash the memory chunk pointer for later use by boost.python
            data->convertible = storage;
        }
};

long sum_coord(bp::tuple t)
{
    Coordinate c = bp::extract<Coordinate>(t);
    return c.x + c.y;
}

void initializeConverters()
{
    // register the to-python converter
    bp::to_python_converter<
        Coordinate,
        Coordinate_to_tuple>();

    // register the from-python converter
    Coordinate_from_tuple();
}

BOOST_PYTHON_MODULE(coordinates) {
    initializeConverters();
    bp::def("sum_coord", sum_coord);
}

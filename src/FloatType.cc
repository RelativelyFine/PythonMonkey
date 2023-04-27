#include "include/FloatType.hh"

#include "include/PyType.hh"
#include "include/TypeEnum.hh"

#include <Python.h>

#include <iostream>


FloatType::FloatType(PyObject *object) : PyType(object) {}

FloatType::FloatType(long n) : PyType(Py_BuildValue("d", (double)n)) {}

FloatType::FloatType(double n) : PyType(Py_BuildValue("d", n)) {}

TYPE FloatType::getReturnType() {
  return TYPE::FLOAT;
}

double FloatType::getValue() const {
  return PyFloat_AS_DOUBLE(pyObject);
}
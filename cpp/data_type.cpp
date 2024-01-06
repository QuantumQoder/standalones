#include <iostream>
#include <string>

using namespace std;

class Person
{
    string name;
    int age;

public:
    Person(string name, int age) : name(name), age(age) {}
    void as_string() { cout << "Person(" << name << ", " << age << ")" << endl; }
};

struct Employee
{
    string name;
    string role;
    Employee(string name, string role) : name(name), role(role) {}
    void as_string() { cout << "Person(" << name << ", " << role << ")" << endl; }
};

// union Employed
// {
//     Person person;
//     Employee employee;
//     Employed(string name, int age) : person(name, age) {}
//     Employed(string name, string role) : employee(name, role) {}
//     void as_string()
//     {
//         person.as_string();
//         employee.as_string();
//     }
// };

// namespace company
// {
//     Person owner;
//     Employee staff;
//     void as_strng()
//     {
//         owner.as_string();
//         staff.as_string();
//     }
// }

int main()
{
    Person person1("Pratik Das", 25);
    person1.as_string();
    Employee employee1("Pratik Das", "Quantum Comm. Team Lead");
    employee1.as_string();
    // company::owner = person1;
    // company::staff = employee1;
    // company::as_strng();
    class Simple
    {
        int value;

    public:
        Simple(int value) : value(value) {}
        void view() { cout << value; }
    } simple1(2);
    simple1.view();
    Simple simple2(3);
    simple2.view();
};
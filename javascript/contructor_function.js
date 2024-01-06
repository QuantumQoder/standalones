// function Person(first, last, age) {
//     this.name = () => first + " " + last;
//     this.age = age
//     function view() {
//         console.log(this)
//     }
//     // this.view = function () {
//     //     console.log(this)
//     // }
// }

class Person {
    constructor(first, last, age) {
        this.name = () => first + " " + last;
        this.age = age
    }
    view() {
        console.log(this)
    }
}

const person1 = new Person("Pratik", "Das", 25)
person1.view()
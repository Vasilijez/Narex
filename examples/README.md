# Examples

- [characters](/examples/characters/) - Match exact characters.
- [coefficients](/examples/coefficients/) - Match all the coefficients of x².
- [date](/examples/date/) - Match various date formats and capture the year.
- [email](/examples/email/) - Match a valid email format.
- [file](/examples/file/) - Match a file with the correct format.
- [positive_numbers](/examples/positive_numbers/) - Match all positive numbers.
- [price](/examples/price/) - Match price formats.
- [repeated_numbers](/examples/repeated_numbers/) - Match repeated numbers from the beginning and the end.
- [simple_number](/examples/simple_number/) - Match a simple number.

Each example includes source code written in Narex, the generated code, and a brief analysis.

If you want to try an example, follow these steps:
1. Navigate to the example directory:
``` sh
cd examples
cd date
```
2a. Generate code using Narex:
``` sh
narex run --path=date.nx --engine=python --overwrite
```
2b. Generate code using textX:
``` sh
textx generate date.nx --target python --overwrite
```
That's it! You can now find the generated code in `date.py`.
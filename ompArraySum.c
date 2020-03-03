/* ompArraySum.c uses an array to sum the values in an input file,
 *  whose name is specified on the command-line.
 * Casper Smet, Huib Aldewereld, HU, HPP, 2020
 * 
 * Compile by gcc -o ompArraySum -fopenmp ompArraySum.c
 * Usage: ./ompArraySum [FILENAME]
 */

#include <stdio.h>      /* I/O stuff */
#include <stdlib.h>     /* calloc, etc. */
#include <omp.h>        /* OpenMP */
#include <math.h>       /* fabs*/

void readArray(char * fileName, double ** a, int * n);
double sumArray(double * a, int numValues);
double paralellArray(double * a, int numValues, int numThreads);
// TODO Remove need for commandline arguments
// TODO Write to file, csv
// TODO Analyse data with excel
int main(int argc, char * argv[])
{
  int  howMany;
  double sum;
  double serial_sum;
  double * a;

  if (argc != 2) {
    fprintf(stderr, "\n*** Usage: arraySum <inputFile>\n\n");
    exit(1);
  }
  readArray(argv[1], &a, &howMany);

  double start = omp_get_wtime();
  sum = paralellArray(a, howMany, 4);
  double end = omp_get_wtime();
  double exec_time = end - start;

  printf("The sum of the values in the input file '%s' is %g\n",
           argv[1], sum); 
  printf("Parallel execution time: %f\n", exec_time);


  double serial_start = omp_get_wtime();
  serial_sum = sumArray(a, howMany);
  double serial_end = omp_get_wtime();
  double serial_exec_time = serial_end - serial_start;
  printf("Serial execution time: %f\n", serial_exec_time);

  double abs_diff = fabs(serial_exec_time - exec_time);
  printf("Absolute difference: %f\n", abs_diff);
  

  free(a);

  return 0;
}

/* readArray fills an array with values from a file.
 * Receive: fileName, a char*,
 *          a, the address of a pointer to an array,
 *          n, the address of an int.
 * PRE: fileName contains N, followed by N double values.
 * POST: a points to a dynamically allocated array
 *        containing the N values from fileName
 *        and n == N.
 */

void readArray(char * fileName, double ** a, int * n) {
  int count, howMany;
  double * tempA;
  FILE * fin;

  fin = fopen(fileName, "r");
  if (fin == NULL) {
    fprintf(stderr, "\n*** Unable to open input file '%s'\n\n",
                     fileName);
    exit(1);
  }

  fscanf(fin, "%d", &howMany);
  tempA = calloc(howMany, sizeof(double));
  if (tempA == NULL) {
    fprintf(stderr, "\n*** Unable to allocate %d-length array",
                     howMany);
    exit(1);
  }

  for (count = 0; count < howMany; count++)
   fscanf(fin, "%lf", &tempA[count]);

  fclose(fin);

  *n = howMany;
  *a = tempA;
}

/* sumArray sums the values in an array of doubles.
 * Receive: a, a pointer to the head of an array;
 *          numValues, the number of values in the array.
 * Return: the sum of the values in the array.
 */

double sumArray(double * a, int numValues) {
  int i;
  double result = 0.0;
  
  for (i = 0; i < numValues; i++) {
    result += a[i];
  }

  return result;
}


double paralellArray(double * a, int numValues, int numThreads) {
  int i;
  double result = 0.0;
  #pragma omp paralell for reduction(+:sum) num_threads(numThreads)
  for (i = 0; i < numValues; i++) {
    result += a[i];
  }

  return result;
}


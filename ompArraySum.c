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
double paralellSumArray(double * a, int numValues, int numThreads);

void testTime(char * fileName);
double * testSerial(double * a, int numValues);
double ** testParalell(double * a, int numValues);


// TODO Remove need for commandline arguments
// TODO Write to file, csv
// TODO Analyse data with excel
int main(int argc, char * argv[])
{
  // char files[4][5] = {"010k", "100k", "001m", "010m"};
  // int i;
  // for (i = 0; i < 4; i++) {
  //   printf("%s", files[i]);
  //   // testTime(files[i]);
  // } 
  testTime("010k");
  return 0;
}

double * testSerial(double * a, int numValues) {
  // Time and run serial
  double sTimes[2];

  sTimes[0] = omp_get_wtime();
  sumArray(a, numValues);
  sTimes[1] = omp_get_wtime();

  return sTimes;
}

double ** testParalell(double * a, int numValues) {
  int i;
  double pTimes[4][2];

  int threadOptions[4] = {1, 2, 4, 8};
  int threadOption;
  for (i = 0; i < 4; i++) {
    threadOption = threadOptions[i];
    // Start time
    pTimes[i][0] = omp_get_wtime();
    paralellSumArray(a, numValues, threadOption);
    // End time
    pTimes[i][1] = omp_get_wtime();
  }

  return pTimes;
}

void testTime(char * fileName) {
  // Variables for collecting array
  int howMany;
  double * a;
  
  
  // Variables for timing
  double ** pTimes;
  double * sTimes;


  readArray(fileName, &a, &howMany);

  // Time and run parallel
  pTimes = testParalell(a, howMany);
  // Time and run serial
  sTimes = testSerial(a, howMany);

  free(a);

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


double paralellSumArray(double * a, int numValues, int numThreads) {
  int i;
  double result = 0.0;

  // #pragma omp paralell for reduction(+:result)
  #pragma omp paralell for reduction(+:result) num_threads(numThreads)
  for (i = 0; i < numValues; i++) {
    result += a[i];
    // printf("%d %d\n", omp_get_thread_num(), omp_get_num_threads());
  }

  return result;
}


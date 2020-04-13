/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   benchmark.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: niragne <niragne@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/04/11 11:46:58 by niragne           #+#    #+#             */
/*   Updated: 2020/04/13 22:02:38 by niragne          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include <time.h>
#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>

#ifndef MEDIUM_TEST_LENGTH
# define MEDIUM_TEST_LENGTH 100
#endif

#ifndef MEDIUM_TEST_SIZE
# define MEDIUM_TEST_SIZE USHRT_MAX
#endif

char *ft_rgb2hex(int r, int g, int b);

struct test_s
{
	int r;
	int g;
	int b;
	char*	ret;
};

struct test_s easy[] =
{
	{0, 0, 0, "#000000"},
	{0, 1, 0, "#000100"},
	{0xff, 0xff, 0xff, "#ffffff"},
	{0x00, 0xff, 0xff, "#00ffff"},
	{0xff, 0x00, 0xff, "#ff00ff"},
	{0xff, 0xff, 0x00, "#ffff00"},
	{0x0a, 0x0a, 0x0a, "#0a0a0a"},
};

int	easy_tests(void)
{
	int failed = 0;
	clock_t start;
	clock_t stop;
	clock_t diff;
	double seconds;

	start = clock();
	
	int i = 0;
	while (i < (sizeof(easy) / sizeof(struct test_s)))
	{
		char* ret = ft_rgb2hex(easy[i].r, easy[i].g, easy[i].b);
		if (strcmp(ret, easy[i].ret))
		{
			failed++;
			printf("Test %d: KO (expected %s)\n", i, easy[i].ret, ret);
		}
		else
			printf("Test %d: OK\n", i);
		free(ret);
		i++;
	}

	stop = clock();
	diff = stop - start;
	seconds = (float)diff / CLOCKS_PER_SEC;
	if (failed == 0)
		printf("easy tests passed in %f\n",seconds);
	else
		printf("easy tests ended in %f with %d failed tests\n", seconds, failed);
	return (failed);
}

int	medium_tests(void)
{
	int i = 0;
	int failed = 0;

	clock_t start;
	clock_t stop;
	clock_t diff;
	clock_t total_time = 0;
	double seconds;

	while (i < MEDIUM_TEST_LENGTH)
	{
		start = clock();
		stop = clock();
		diff = stop - start;
		total_time += diff;
		i++;
	}
	seconds = (float)total_time / CLOCKS_PER_SEC;
	
	if (failed == 0)
		printf("medium tests passed in %f\n",seconds);
	else
		printf("medium tests ended in %f with %d failed tests\n", seconds, failed);
	
	return (failed);
}

int main(int ac, char** av)
{
	int ret = 0;
	// srand(time(NULL));
	printf("EASY TESTS:\n");
	ret += easy_tests();
	printf("\n");
	return (ret);
}
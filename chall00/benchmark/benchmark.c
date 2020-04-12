/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   benchmark.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: niragne <niragne@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/04/11 11:46:58 by niragne           #+#    #+#             */
/*   Updated: 2020/04/12 14:08:31 by niragne          ###   ########.fr       */
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

int ft_necklace(char *s1, char *s2);

struct test_s
{
	char*	s1;
	char*	s2;
	int			ret;
};

struct test_s easy[] =
{
	{"salut", "bonsoir", 0},
	{"nicole", "icolen", 1},
	{"nicole", "lenico", 1},
	{"nicole", "coneli", 0},
	{"aabaaaaabaab", "aabaabaabaaa", 1},
	{"abc", "cba", 0},
	{"xxyyy", "xxxyy", 0},
	{"xyxxz", "xxyxz", 0},
	{"x", "x", 1},
	{"x", "xx", 0},
	{"x", "", 0},
	{":)", "):", 1},
	{"", "s", 0},
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
		if (ft_necklace(easy[i].s1, easy[i].s2) != easy[i].ret)
		{
			failed++;
			printf("Test %d: KO\n", i);
		}
		else
			printf("Test %d: OK\n", i);
		
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
	char	s1[MEDIUM_TEST_SIZE];
	char	s2[MEDIUM_TEST_SIZE];

	clock_t start;
	clock_t stop;
	clock_t diff;
	clock_t total_time = 0;
	double seconds;

	memset(s1, 'A', sizeof(s1));
	memset(s2, 'A', sizeof(s2));
	s1[sizeof(s1) - 1] = 0;
	s2[sizeof(s2) - 1] = 0;

	while (i < MEDIUM_TEST_LENGTH)
	{
		int index1 = rand() % sizeof(s1 - 1);
		int index2 = rand() % sizeof(s2 - 1);
		s1[index1] = 'B';
		s2[index2] = 'B';
		
		start = clock();
		if (ft_necklace(s1, s2) != 1)
			failed++;
		stop = clock();
		diff = stop - start;
		total_time += diff;
		s1[index1] = 'A';
		s2[index2] = 'A';
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
	printf("MEDIUM TESTS:\n");
	ret += medium_tests();
	printf("\n");
	return (ret);
}
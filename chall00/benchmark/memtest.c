/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memtest.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: niragne <niragne@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/04/12 12:42:31 by niragne           #+#    #+#             */
/*   Updated: 2020/04/12 12:43:51 by niragne          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int ft_necklace(char *s1, char *s2);


int main(int ac, char** av)
{
	char	s1[255];
	char	s2[255];
	memset(s1, 'A', sizeof(s1));
	memset(s2, 'A', sizeof(s2));
	s1[sizeof(s1) - 1] = 0;
	s2[sizeof(s2) - 1] = 0;
	ft_necklace(s1, s2);
	return (0);
}
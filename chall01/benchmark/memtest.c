/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   memtest.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: niragne <niragne@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/04/12 12:42:31 by niragne           #+#    #+#             */
/*   Updated: 2020/04/13 21:48:51 by niragne          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

char *ft_rgb2hex(int r, int g, int b);

int main(int ac, char** av)
{
	char* s =  ft_rgb2hex(0, 0xa, 0xff);
	free(s);
	return (0);
}
/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   process_data.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 17:25:18 by ecross            #+#    #+#             */
/*   Updated: 2020/02/28 17:39:56 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int		process(char *data_file)
{
	int				fd;
	t_data_struct	s;

	if ((fd = open(data_file, O_RDONLY)) < 0)
	{
		ft_putstr_fd("Error opening data file.\n", 1);
		return (0);
	}
	close(data_file);
	return (1);
}

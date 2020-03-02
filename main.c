/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/27 16:41:12 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 12:02:28 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	main(void)
{
	char	buff[BUFF_SIZE];

	/*read_sheet(buff, "../install.csv");
	if(!get_install_data(buff, "../data.txt"))
		return (1);
	read_sheet(buff, "../project.csv");
	if(!get_project_data(buff, "../data.txt"))
		return (1);*/
	process("../data.txt");
	return (0);
}

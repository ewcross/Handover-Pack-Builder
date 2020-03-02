/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/27 16:41:12 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 12:46:46 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int	main(void)
{
	char			buff[BUFF_SIZE];
	t_data_struct	s;

	/*read_sheet(buff, "../install.csv");
	if(!get_install_data(buff, "../data.txt"))
		return (1);
	read_sheet(buff, "../project.csv");
	if(!get_project_data(buff, "../data.txt"))
		return (1);*/
	process(&s, "../data.txt");
	
	printf("job       TL%s\n", s.job);
	printf("cust known %d\n", s.cust_known);
	printf("locations %d\n", s.locations);
	printf("mpan %d\n", s.mpan);
	printf("phases %d\n", s.phases);
	printf("dno %d\n", s.dno_app);
	printf("monitoring %d\n", s.monitoring);
	printf("commercial %d\n", s.commercial);
	
	get_files(&s);
	return (0);
}

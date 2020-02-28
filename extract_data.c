/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   extract_data.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:33:19 by ecross            #+#    #+#             */
/*   Updated: 2020/02/28 17:04:21 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int		get_value(char *buff, char *res, char *mark, int instance, int cells_after, int fd)
{
	int		i;
	int		j;
	int		ret;
	char	*pos;

	j = 0;
	ret = 0;
	pos = buff;
	i = 0;
	while (i < instance)
	{
		if(!(pos = strstr(pos, mark)))
		{
			res[j++] = 10;
			res[j] = 0;
			return (0);
		}
		pos++;
		i++;
	}
	i = 0;
	while (i < cells_after)
	{
		while (*pos != ',')
			pos++;
		pos++;
		i++;
	}
	while (*pos != ',')
	{
		res[j++] = *pos;
		ret++;
		pos++;
	}
	res[j++] = 10;
	res[j] = 0;
	return(ret);
}

int		get_install_data(char *buff, char *output_file)
{
	int		fd;
	char	*command;
	char	data[200];

	/*system calls will need to be edited for Windows*/
	command = ft_strjoin("rm ", output_file);
	system(command);
	if ((fd = open(output_file, O_WRONLY|O_CREAT)) < 0)
	{
		ft_putstr_fd("Error creating data file.\n", 1);
		return (0);
	}
	command = ft_strjoin("chmod 777 ", output_file);
	system(command);

	data[0] = 0;
	ft_putstr_fd("Job:                   T", fd);
	get_value(buff, data, "TL", 1, 0, fd);
	ft_putstr_fd(data, fd);
	
	ft_putstr_fd("1   Customer name:     ", fd);
	get_value(buff, data, "TL", 1, 1, fd);
	ft_putstr_fd(data, fd);

	ft_putstr_fd("2   Inverter location: ", fd);
	get_value(buff, data, "Location of Inverter", 2, 1, fd);
	ft_putstr_fd(data, fd);
	
	if(!get_value(buff, data, "Location of TGM", 2, 1, fd))
	{
		ft_putstr_fd("3   CU location:       ", fd);
		get_value(buff, data, "Location of CU", 1, 1, fd);
	}
	else
	{
		ft_putstr_fd("3   TGM location:      ", fd);
	}
	ft_putstr_fd(data, fd);

	ft_putstr_fd("4   Monitoring value:  ", fd);
	get_value(buff, data, "Monitoring", 1, 1, fd);
	ft_putstr_fd(data, fd);
	
	ft_putstr_fd("5   DNO pre_app:       ", fd);
	get_value(buff, data, "DNO", 1, 1, fd);
	ft_putstr_fd(data, fd);
	
	ft_putstr_fd("6   MPAN:              ", fd);
	get_value(buff, data, "MPAN", 1, 1, fd);
	ft_putstr_fd(data, fd);
	
	ft_putstr_fd("7   Panels:            ", fd);
	get_value(buff, data, "PV Panel Desc", 2, 1, fd);
	ft_putstr_fd(data, fd);

	ft_putstr_fd("8   Inverter:          ", fd);
	get_value(buff, data, "Inverter", 12, 1, fd);
	ft_putstr_fd(data, fd);
	
	ft_putstr_fd("9   EIC or DC/AC:      ", fd);
	get_value(buff, data, "Full EIC or", 1, 1, fd);
	ft_putstr_fd(data, fd);

	close(fd);
	return (1);
}
int		get_project_data(char *buff, char *output_file)
{
	int		fd;
	char	data[200];

	data[0] = 0;
	if ((fd = open(output_file, O_WRONLY | O_APPEND)) < 0)
	{
		ft_putstr_fd("Error opening data file.\n", 1);
		return (0);
	}
	ft_putstr_fd("10  Phases:            ", fd);
	get_value(buff, data, "Phases", 1, 1, fd);
	ft_putstr_fd(data, fd);
	ft_putstr_fd("11  Dom or Com:        ", fd);
	get_value(buff, data, "Property Type", 1, 1, fd);
	ft_putstr_fd(data, fd);
	close(fd);
	return (1);
}

int		read_sheet(char *buff, char *file)
{
	int	fd;
	int	bytes;

	if ((fd = open(file, O_RDONLY)) < 0)
	{
		ft_putstr_fd("Error opening file.\n", 1);
		return (0);
	}
	bytes = read(fd, buff, BUFF_SIZE);
	if (bytes < 0)
	{
		ft_putstr_fd("Error reading file.\n", 1);
		close(fd);
		return (0);
	}
	close(fd);
	return (1);
}

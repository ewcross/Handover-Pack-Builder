/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:34:10 by ecross            #+#    #+#             */
/*   Updated: 2020/02/28 17:35:37 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "libgnl.h"
#include "libft.h"

# define BUFF_SIZE 100000

typedef struct	s_data_struct
{
	int			locations;
	int			mpan;
	int			phases;
	char		dno_app;
	char		cust_known;
	char		commercial;
	char		job[4];
}				t_data_struct;

int		get_value(char *buff, char *res, char *mark, int instance, int cells_after, int fd);
int		get_install_data(char *buff, char *output_file);
int		get_project_data(char *buff, char *output_file);
int		read_sheet(char *buff, char *file);
int		process(char *data_file);

#endif

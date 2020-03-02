/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:34:10 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 12:39:43 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef HEADER_H
# define HEADER_H

#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include "libgnl.h"
#include "libft.h"

# define BUFF_SIZE 100000
# define SMALL_BUFF_SIZE 1500

typedef struct	s_data_struct
{
	int			locations;
	int			mpan;
	int			phases;
	bool		dno_app;
	bool		monitoring;
	bool		cust_known;
	bool		commercial;
	char		job[5];
}				t_data_struct;

int		get_value(char *buff, char *res, char *mark, int instance, int cells_after, int fd);
int		get_install_data(char *buff, char *output_file);
int		get_project_data(char *buff, char *output_file);
int		read_sheet(char *buff, char *file);
int		process(char *data_file);

#endif

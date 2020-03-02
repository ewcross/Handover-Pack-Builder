/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:34:10 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 13:01:03 by ecross           ###   ########.fr       */
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

/*
**Include here all relevant paths to template files
*/

# define COVER_SHEET "../templates/01_cover.txt"
# define HOP_FOLDER "../current"

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
int		get_job_no(t_data_struct *s, char *buff);
char	*make_str(char *start, char *finish);
char	*get_string(char *buff, char *mark);
int		same_str(char *s1, char *s2);
void	get_mpan(t_data_struct *s, char *mpan);
void	get_phase(t_data_struct *s, char *phases);
void	set_bool_if_match(bool *on, char *str, char *match);
int		get_struct_data(t_data_struct *s, char *buff);
int		process(t_data_struct *s, char *data_file);
int		get_files(t_data_struct *s);

#endif

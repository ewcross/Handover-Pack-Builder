/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:34:10 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 14:36:25 by ecross           ###   ########.fr       */
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
# define LAST_PAGE "../templates/08_general.txt"

# define CUSTOMER "../templates/02_customer.txt"
# define NO_CUSTOMER "../templates/02_no_customer.txt"

# define VIS_ONE_PHASE_ONE_LOC "../templates/03_1_1.txt"
# define VIS_ONE_PHASE_TWO_LOC "../templates/03_1_2.txt"
# define VIS_THREE_PHASE_ONE_LOC "../templates/03_3_1.txt"
# define VIS_THREE_PHASE_TWO_LOC "../templates/03_3_2.txt"

# define PV_OP_ONE_LOC "../templates/04_1.txt"
# define PV_OP_TWO_LOC "../templates/04_2.txt"

# define COMMERCIAL "../templates/04b_commercial.txt"

# define SIX_G99_10_12_19_28 "../templates/06_99_10_12_19_28.txt"
# define SIX_G99_20 "../templates/06_99_27.txt"
# define SIX_G99_25 "../templates/06_99_27.txt"
# define SIX_G99_27 "../templates/06_99_27.txt"
# define SIX_G98_10_12_19_28 "../templates/06_98_10_12_19_28.txt"
# define SIX_G98_25 "../templates/06_98_25.txt"
# define SIX_G98_20 "../templates/06_98_20.txt"

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

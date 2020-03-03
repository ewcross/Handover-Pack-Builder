/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   header.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 16:34:10 by ecross            #+#    #+#             */
/*   Updated: 2020/03/03 14:24:21 by ecross           ###   ########.fr       */
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
**Spaces in file names MUST be escaped
*/

# define COVER_SHEET "../templates/01**Coversheet*"
# define LAST_PAGE "../templates/08**Warranty*"

# define CUSTOMER "../templates/02**Coveringletter.*"
# define NO_CUSTOMER "../templates/02**Coveringletter_No_Customer.*"

# define VIS_ONE_PHASE_ONE_LOC "../templates/03**1**1*"
# define VIS_ONE_PHASE_TWO_LOC "../templates/03**1**2*"
# define VIS_THREE_PHASE_ONE_LOC "../templates/03**3**1*"
# define VIS_THREE_PHASE_TWO_LOC "../templates/03**3**2*"

# define PV_OP_ONE_LOC "../templates/04**Location.*"
# define PV_OP_TWO_LOC "../templates/04**Locations*"

# define COMMERCIAL "../templates/04b*"

# define G99_10_12_19_28 "../templates/06**G99**10_12_19_28*"
# define G99_20 "../templates/06**G99**20*"
# define G99_25 "../templates/06**G99**25*"
# define G99_27 "../templates/06**27**G99*"

# define G98_10_12_19_28 "../templates/06**G98**10_12_19_28*"
# define G98_25 "../templates/06**G98**25*"
# define G98_20 "../templates/06**G98**20**"

# define HOP_FOLDER "../current"

/*Extra docs
"../templates/03 Template 3 Phase 1 Location Integrated Meter PV Electrical Schematic.vsdx"
"../templates/03 Template Micro-Inverter PV Electrical Schematic.vsdx"
"../templates/06 Template ESPE G99 Form A3-1 issue 1 amd 3.docx"
"../templates/06 Template SSEG G98 Form B Installation Document for connection.docx"
"../templates/07 Template PV Array & AC Circuit Test Only.docx"
"../templates/07 Template PV Array Test Only.docx"
"../templates/07 Template_EIC(2019-3).docx"
"../templates/07 Template_EIC(2020-1).docx"
*/

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

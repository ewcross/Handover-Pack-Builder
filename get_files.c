/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_files.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/03/02 12:46:56 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 14:32:19 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int		copy_file(char *file)
{
	char	*p1;
	char	*p2;

	/*will need to handle return values of system call*/
	p1 = ft_strjoin("cp ", file);
	p2 = ft_strjoin(p1, " ");
	free(p1);
	p1 = ft_strjoin(p2, HOP_FOLDER);
	free(p2);
	if(system(p1))
	{
		ft_putstr_fd("Error copying file ", 1);
		ft_putstr_fd(file, 1);
		ft_putstr_fd(".\n", 1);
	}
	free(p1);
	return (1);
}

int		visio_and_pv_op(t_data_struct *s)
{
	if (s->locations == 1)
	{
		copy_file(PV_OP_ONE_LOC);
		if (s->phases == 1)
			copy_file(VIS_ONE_PHASE_ONE_LOC);
		else if (s->phases == 3)
			copy_file(VIS_THREE_PHASE_ONE_LOC);
	}
	else if (s->locations == 2)
	{
		copy_file(PV_OP_TWO_LOC);
		if (s->phases == 1)
			copy_file(VIS_ONE_PHASE_TWO_LOC);
		else if (s->phases == 3)
			copy_file(VIS_THREE_PHASE_TWO_LOC);
	}
	return (1);
}

int		six_doc(t_data_struct *s)
{
	if (s->dno_app)
	{
		copy_file(SIX_G99_20);
	}
	else if (!s->dno_app)
	{
		copy_file(SIX_G98_20);
	}
	return (1);
}

int		get_files(t_data_struct *s)
{
	char	*p1;
	char	*p2;

	copy_file(COVER_SHEET);
	if (s->cust_known)
		copy_file(CUSTOMER);
	else
		copy_file(NO_CUSTOMER);
	visio_and_pv_op(s);
	six_doc(s);
	if (s->commercial)
		copy_file(COMMERCIAL);
	copy_file(LAST_PAGE);
	return (1);
}

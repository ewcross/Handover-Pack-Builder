/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_files.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/03/02 12:46:56 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 13:01:31 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int		get_files(t_data_struct *s)
{
	char	*p1;
	char	*p2;

	/*will need to handle return values of system calls here*/
	p1 = ft_strjoin("cp ", COVER_SHEET);
	p2 = ft_strjoin(p1, " ");
	free(p1);
	p1 = ft_strjoin(p2, HOP_FOLDER);
	free(p2);
	system(p1);
	free(p1);
	return (1);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   process_data.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2020/02/28 17:25:18 by ecross            #+#    #+#             */
/*   Updated: 2020/03/02 12:43:40 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "header.h"

int		get_job_no(t_data_struct *s, char *buff)
{
	int		i;
	char	*point;

	point = strstr(buff, "TL");
	if (!point)
		return (0);
	i = 2;
	while (i < 6)
	{
		s->job[i - 2] = *(point + i);
		i++;
	}
	s->job[i - 2] = 0;
	return (1);
}

char	*make_str(char *start, char *finish)
{
	int		i;
	int		len;
	char	*new;

	len = finish - start + 1;
	new = (char*)malloc(len + 1);
	if (!new)
		return (NULL);
	new[len] = 0;
	while (i < len)
	{
		new[i] = start[i];
		i++;
	}
	return (new);
}

char	*get_string(char *buff, char *mark)
{
	int		i;
	char	*start;
	char	*finish;

	start = strstr(buff, mark);
	if (!start)
	{
		ft_putstr_fd("Could not find mark.\n", 1);
		return (NULL);
	}
	while (*start != ':')
		start++;
	start++;
	while (*start == ' ' || *start == 9)
		start++;
	finish = start;
	while (*finish != 10)
		finish++;
	finish--;
	while (*finish == ' ')
		finish--;
	return (make_str(start, finish));
}

int		same_str(char *s1, char *s2)
{
	int		i;

	i = 0;
	while (s1[i] && s2[i])
	{
		if (s1[i] != s2[i])
		{
			if ((s1[i] > 96 && s1[i] < 123 && s1[i] - 32 == s2[i]) ||
					(s1[i] > 64 && s1[i] < 91 && s1[i] + 32 == s2[i]))
			{
				i++;
				continue ;
			}
			else
				return (0);
		}
		i++;
	}
	return (1);
}

void	get_mpan(t_data_struct *s, char *mpan)
{
	char	digits[3];
	
	digits[0] = mpan[0];
	digits[1] = mpan[1];
	digits[2] = 0;
	s->mpan = ft_atoi(digits);
	free(mpan);
}

void	get_phase(t_data_struct *s, char *phases)
{
	if (same_str(phases, "Single phase"))
		s->phases = 1;
	else if (same_str(phases, "3 Phase"))
		s->phases = 3;
	else
		s->phases = 0;
	free(phases);
}

void	set_bool_if_match(bool *on, char *str, char *match)
{
	if (same_str(str, match))
		*on = 1;
	else
		*on = 0;
	free(str);
}

int		get_struct_data(t_data_struct *s, char *buff)
{
	char	*loc1;
	char	*loc2;

	if(!get_job_no(s, buff))
		ft_putstr_fd("Could not get job number.\n", 1);
	/*can maybe change bool flips when opposite id is known*/
	set_bool_if_match(&(s->cust_known), get_string(buff, "#1"), "no");
	s->cust_known = !s->cust_known;
	loc1 = get_string(buff, "#2");
	loc2 = get_string(buff, "#3");
	if(same_str(loc1, loc2))
		s->locations = 1;
	else
		s->locations = 2;
	get_mpan(s, get_string(buff, "#6"));
	get_phase(s, get_string(buff, "#10"));
	set_bool_if_match(&(s->dno_app), get_string(buff, "#5"), "Yes");
	set_bool_if_match(&(s->monitoring), get_string(buff, "#4"), "not installed");
	s->monitoring = !s->monitoring;
	set_bool_if_match(&(s->commercial), get_string(buff, "#11"), "commercial");
	free(loc1);
	free(loc2);
	return (1);
}

int		process(t_data_struct *s, char *data_file)
{
	int				fd;
	int				bytes;
	char			buff[SMALL_BUFF_SIZE];

	if ((fd = open(data_file, O_RDONLY)) < 0)
	{
		ft_putstr_fd("Error opening data file.\n", 1);
		return (0);
	}
	bytes = read(fd, buff, SMALL_BUFF_SIZE);
	close(fd);
	if (bytes < 0)
	{
		ft_putstr_fd("Error reading file.\n", 1);
		return (0);
	}
	get_struct_data(s, buff);
	return (1);
}

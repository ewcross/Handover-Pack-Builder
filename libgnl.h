/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ecross <marvin@42.fr>                      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/10/21 19:07:39 by ecross            #+#    #+#             */
/*   Updated: 2019/10/29 10:15:22 by ecross           ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <fcntl.h>
# include <unistd.h>
# include <stdlib.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 100
# endif

typedef	struct	s_struct
{
	char		res_chars[BUFFER_SIZE];
	int			n_chars;
	int			processed;
	int			fd;
}				t_gnl;

int				move_chars(char *src, char *dest, int start, int end);
void			write_backwards(char *line, char *buff, int n, int count);
int				get_next_line(int fd, char **line);
int				fill_buff(t_gnl *s_struct, char *buff);
int				search(char **line, char *buff, int *addr_count, int *i_byt);
char			*make(t_gnl *s_struct, char *buff, int count, int *i_byt);
int				gnl_rec(t_gnl *s_struct, char **line, int count);
#endif
